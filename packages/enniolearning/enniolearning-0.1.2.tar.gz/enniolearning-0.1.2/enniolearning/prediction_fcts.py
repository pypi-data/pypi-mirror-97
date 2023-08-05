from enniolearning.utils import FindMaxLength, reject_for_repetition
from enniolearning.training_fcts import deserialize_score, deserialize_general_note, list_model_files, to_tensor, prepare_sequences, device, reuse_network, get_serialized_model_filename_by_epoch, get_serialized_model_name_by_filename, load_network, parse_epoch
import numpy as np
import matplotlib.pyplot as plt
import pickle
from enniolearning.eta_tools import EtaPrinter, get_progress_ratio
from music21.note import Rest

SKIP_LOSS_FUNCTION = 'Skip Loss Function'
SKIP_LEARNING_RATE = 'Skip Learning Rate'
SKIP_MODEL_FILE = 'Skip Model File'
STATUS_TYPE_ETA = 'eta'


def evaluate_generated_score(prediction_by_track, network_input, enable_evaluation=True,
                             repetition_by_track_ratio_accepted=0.4, **kwargs):

    if not enable_evaluation:
        return 0, False

    # remove split by batch
    flatten_input = network_input.reshape((network_input.shape[0] * network_input.shape[1], network_input.shape[2]))
    #     assert flatten_input.shape[1] == prediction.shape[1] #number of parts (~instruments)
    # https://stackoverflow.com/questions/48828270/dynamic-programming-w-pytorch-longest-common-subsequence #to_tensor tout con met trop de temps (arrêté au bout de plusieurs minutes, alors que cpu met 49sec)

    # plagia : evaluate copy of input dataset
    plagia_part = 0
    for track_idx in range(flatten_input.shape[1]):
        plagia_part = max(plagia_part, FindMaxLength(flatten_input[:][track_idx], prediction_by_track[track_idx]))
    #     print(f"Evaluation : morceau généré à {100 * (len(prediction) - plagia_part)/len(prediction)}%")

    # Repetition detection : not pleasant to here
    rejected_by_track = np.array(
        [reject_for_repetition(prediction_by_track[track_idx]) for track_idx in range(len(prediction_by_track))])
    rejected_for_repetition = np.sum(rejected_by_track == True) / len(
        rejected_by_track) > repetition_by_track_ratio_accepted

    return plagia_part, rejected_for_repetition


def create_generation_input(previous_prediction_output_as_int=None, network_input=None, **kwargs):
    if previous_prediction_output_as_int is not None:
        print('From previous prediction')
        return previous_prediction_output_as_int # shape=(generate_output_length, nb_instruments)
    if network_input is not None:
        # pick a random sequence from the input as a starting point for the prediction
        start = np.random.randint(0, len(network_input) - 1)
        return network_input[start]  # shape=(sequence_length,nb_instruments)
    raise KeyError('Must provide at least one of [previous_prediction_output_as_int, network_input]')


def generate_notes(model, int_to_note, n_vocab,  generate_output_length=50, **kwargs):
    """ Generate notes from the neural network based on a sequence of notes.
    Dim 0 = time sequence (generate_output_length) ; Dim 1 = instrument index.
    """
    pattern = create_generation_input(**kwargs)
    prediction_output = []
    prediction_output_as_int = []
    # generate generate_output_length notes
    for note_index in range(generate_output_length):
        #         print('pattern', pattern)
        prediction_input = np.reshape(pattern, (1, pattern.shape[0], pattern.shape[1]))  # shape (1,sequence_length,len(instrument_index))
        prediction_input = prediction_input / float(n_vocab)
        prediction_input = to_tensor(prediction_input)
        prediction = model(prediction_input)  # shape (1,n_vocab,len(instrument_index)) (=len(int_to_note))
        if prediction.shape[0] != 1:
            print(
                f"expected batch output size == 1, was {prediction.shape[0]}")  # could it be some feature to return several sequence in a batch (batch_size > 1) -> check perf
        prediction = prediction.squeeze(0)  # ignore 1st dimension (batch index)
        next_note_as_int = []
        next_note = []
        for instrument_prediction in prediction:
            next_note_as_int_by_instrument = instrument_prediction.argmax().item()
            next_note_by_instrument = int_to_note[next_note_as_int_by_instrument]
            next_note_as_int.append(next_note_as_int_by_instrument)
            next_note.append(next_note_by_instrument)

        prediction_output_as_int.append(next_note_as_int)
        prediction_output.append(next_note)
        next_note_as_int = np.array(next_note_as_int).reshape(1, (len(next_note_as_int)))
        pattern = np.vstack((pattern[1:], next_note_as_int))  # along with dim 0 : time sequence

    return np.array(prediction_output), np.array(prediction_output_as_int)


def create_midi(prediction_output, instruments_index,
                create_midi_file=False, output_filename='default_output.mid',
                start_playback=False, show_part=False, **kwargs):
    """ convert the output from the prediction to notes and create a midi file
        from the notes """
    midi_stream = deserialize_score(prediction_output, instruments_index)
    if show_part:
        midi_stream.show()
    if start_playback:
        midi_stream.show('midi')
    if create_midi_file:
        midi_stream.write('midi', fp=output_filename)
        # print(f"File {output_filename} created !")
        return output_filename
    return None

def is_a_rest(general_note, **kwargs):
    # TRY perf ? return general_note == PADDING_STR or 'R_' in general_note
    return type(deserialize_general_note(general_note, **kwargs)) is Rest


def is_all_instrument_rest(all_instrument_prediction, **kwargs) -> bool:
    for general_note in all_instrument_prediction:
        if not is_a_rest(general_note, **kwargs):
            return False
    return True


def ignore_few_note(prediction, i, min_no_rest_sequence_accepted, is_rest=False):
    """
    :param prediction:
    :param i: start to analyze from this index
    :param min_no_rest_sequence_accepted:
    :param is_rest:
    :return: [0] True if this note should be ignored because it is isolated between rests
    [1] nb of analyzed indices, so next iteration do not have to process them again
    """
    if is_rest:
        return False, 1 # N/A
    if min_no_rest_sequence_accepted > 1:
        for j in range(1, min_no_rest_sequence_accepted): # because i is already known as non-rest
            index_to_analyze = i + j
            if index_to_analyze < len(prediction):
                if is_all_instrument_rest(prediction[index_to_analyze]):
                    return True, j
    return False, min(min_no_rest_sequence_accepted, len(prediction)-i)


def post_processing(prediction_output, prediction_output_as_int, enable_post_processing=True,
                    min_no_rest_sequence_accepted=3, max_rest_sequence_accepted=10, serialize_prediction=False, **kwargs):
    """
    Performs tasks :

    1 - Delete notes being too few in the middle of large all-instruments rests

    2 - Reduce long sequences of all-instruments rests

    :param min_no_rest_sequence_accepted: if before and after a long all-instruments rest,
     sequence of notes (i.e not a all-instruments rest) shorter than this will be skipped.
    :param max_rest_sequence_accepted:
    sequence of all-instruments rests will not exceed this length (so will be shorten if necessary).
    """
    # prediction shape = (generate_output_length, len(instrument_index))
    if serialize_prediction and type(serialize_prediction) is str:
        with open(f"{serialize_prediction}", 'xb') as filepath:
            pickle.dump(prediction_output_as_int, filepath)

    if not enable_post_processing:
        return prediction_output, prediction_output_as_int, 1.0

    generate_output_length = prediction_output.shape[0]
    rest_sequence_len = 0
    rest_step_cumul = []
    should_ignore_note = []
    i = 0
    while i < generate_output_length :
        is_rest = is_all_instrument_rest(prediction_output[i], **kwargs)
        # detect isolated notes only if inside a long rest
        is_isolated_note, step = (False, 1) if rest_sequence_len <= max_rest_sequence_accepted \
            else ignore_few_note(prediction_output, i, min_no_rest_sequence_accepted, is_rest)
        rest_sequence_len = rest_sequence_len+1 if is_rest or is_isolated_note else 0
        if not is_isolated_note:
            rest_step_cumul.extend(rest_sequence_len for _ in range(step))
            should_ignore_note.extend(False for _ in range(step))
            i += step
        else:
            rest_step_cumul.append(rest_sequence_len)
            should_ignore_note.append(is_isolated_note) # True -> prediction will be skipped
            i += 1
    shrink_long_rest_mask = np.array(rest_step_cumul) <= max_rest_sequence_accepted
    should_ignore_note = np.array(should_ignore_note)
    post_processing_indexing = np.logical_and(shrink_long_rest_mask, np.logical_not(should_ignore_note))
    post_processing_score = np.sum(post_processing_indexing) / generate_output_length # kept predicted notes ratio

    if serialize_prediction and type(serialize_prediction) is str:
        with open(f"{serialize_prediction}_postprocessed", 'xb') as filepath:
            pickle.dump(prediction_output_as_int[post_processing_indexing], filepath)

    return prediction_output[post_processing_indexing], prediction_output_as_int[post_processing_indexing], post_processing_score


def generate(notes=None, instruments_index=None, model=None, batch_size=1, network_input=None, int_to_note=None,
             plot_diversity=False, **kwargs):
    """ Generate a piano midi file
    :returns: output_filename, prediction_output_as_int, (diversity_rate, plagia_part, rejected_for_repetition, post_processing_score)
    """
    notes, instruments_index = or_load_from_file(notes, instruments_index, **kwargs)

    lstm_input_size = len(instruments_index)

    if network_input is None or int_to_note is None :
        network_input, _, note_to_int, int_to_note, sequence_length = prepare_sequences(notes,
                                                                                        batch_size=batch_size,
                                                                                        predict_mode=True, **kwargs)
    n_vocab = len(int_to_note)

    model = reuse_network(model, batch_size=batch_size, n_vocab=n_vocab, input_size=lstm_input_size, **kwargs)
    prediction_output, prediction_output_as_int = generate_notes(model,
                                                                 int_to_note,
                                                                 n_vocab,
                                                                 network_input=network_input,
                                                                 **kwargs)

    prediction_output, prediction_output_as_int, post_processing_score = post_processing(prediction_output,
                                                                                         prediction_output_as_int,
                                                                                         **kwargs)

    prediction_output_by_instru = prediction_output.transpose()

    # evaluate prediction
    plagia_part, rejected_for_repetition = evaluate_generated_score(prediction_output_as_int.transpose(),
                                                                    network_input, **kwargs)
    diversity_rate = len(np.unique(prediction_output)) / float(n_vocab)

    if plot_diversity:
        plt.figure(figsize=(18, 4))
        for instru_idx, instru_name in enumerate(instruments_index):
            plt.plot(prediction_output_by_instru[instru_idx], label=instru_name)
        plt.title(f"Prediction diversity : {diversity_rate * 100:.2f}%")
        plt.legend()
        # plt.show()

    output_filename = create_midi(prediction_output_by_instru, instruments_index, **kwargs)

    return output_filename, prediction_output_as_int, (diversity_rate, plagia_part, rejected_for_repetition, post_processing_score)


def or_load_from_file(notes=None, instruments_index=None, dump_path='data', **kwargs):
    if notes is None:
        # load the notes used to train the model
        with open(dump_path+'/notes_by_instrument', 'rb') as filepath:
            notes = pickle.load(filepath)
    if instruments_index is None:
        with open(dump_path+'/instruments_index', 'rb') as filepath:
            instruments_index = pickle.load(filepath)
    return notes, instruments_index


LOSS_FUNCTION = '{0}'
LEARNING_RATE = '{1}'


def evaluate_models(path, exec_nb=1, loss_func_names=['BCELoss()'], lrs=[1e-3, 1e-4, 1e-5], select_epochs=False,
                    generate_output_length=300, print_progress=True, notes=None, instruments_index=None, batch_size=1, jordan_instance=None, **kwargs):
    """Path : use make_path()
    use '{0}' or LOSS_FUNCTION for loss function name
    use '{1}' or LEARNING_RATE" for learning rate
    e.g make_path('my_trainings', 'theme_A', LEARNING_RATE, 'fct-'+LOSS_FUNCTION)
    Will list all files in the path, and predict <exec_nb> times an output of length <generate_output_length>
    Returns an evaluation structure (3-level dict) with keys :
    1 - folder
    2 - model filename
    3 - diversity_rate, plagia_part, rejected_for_repetition
    and values = mean of the <exec_nb> values for each 3rd level keys

    Currently, <loss_func_name> and <lrs> must not be empty (and should be well passed) because loops are based on their content.
    Note <loss_func_name> should include parenthesis (check default value).

    <jordan_instance> handles SKIP_LOSS_FUNCTION, SKIP_LEARNING_RATE and SKIP_MODEL_FILE actions.
    """

    notes, instruments_index = or_load_from_file(notes, instruments_index, **kwargs)
    lstm_input_size = len(instruments_index)

    _, normalized_input, note_to_int, int_to_note, sequence_length = prepare_sequences(notes,
                                                                                                   batch_size=batch_size,
                                                                                                   predict_mode=True)
    n_vocab = len(note_to_int)

    evaluation = {}

    eta = EtaPrinter()
    interrupt_loop, jordan_message = False, None
    for loss_function_passed, loss_func_name in enumerate(loss_func_names):
        for lr_passed, lr in enumerate(lrs):

            # jordan loop control
            if interrupt_loop:
                if jordan_message and jordan_message.action_name == SKIP_LOSS_FUNCTION:
                    jordan_message.processed()
                    jordan_message = None
                    interrupt_loop = False
                break

            subfolder = path.format(loss_func_name, f"{lr:.0E}")
            #             print(f"In folder {subfolder}")
            evaluation[subfolder] = {}

            model_files_in_folder = list_model_files(subfolder)
            model_files = select_models(model_files_in_folder, select_epochs)
            for model_passed, model_filename in enumerate(model_files):

                # jordan loop control
                if interrupt_loop:
                    if jordan_message and jordan_message.action_name == SKIP_LEARNING_RATE:
                        jordan_message.processed()
                        jordan_message = None
                        interrupt_loop = False
                    break

                diversity_rates = []
                plagia_parts = []
                rejected_for_repetitions = []
                post_processing_scores = []
                model_path = get_serialized_model_name_by_filename(subfolder, model_filename)

                model = load_network(model_path, batch_size=batch_size, n_vocab=n_vocab,
                                     input_size=lstm_input_size, **kwargs)

                for i in range(exec_nb):

                    # jordan loop control
                    if interrupt_loop:
                        if jordan_message and jordan_message.action_name == SKIP_MODEL_FILE:
                            jordan_message.processed()
                            jordan_message = None
                            interrupt_loop = False
                        break

                    if print_progress:
                        progress_tuples = (loss_function_passed, len(loss_func_names)),\
                                          (lr_passed, len(lrs)),\
                                          (model_passed, len(model_files)),\
                                          (i, exec_nb)
                        eta_as_string = eta.print_eta(*progress_tuples)
                        general_progress = f"Loss function = {loss_func_name} ({get_percent(loss_function_passed + 1, len(loss_func_names))})," \
                                   f" LR = {lr} ({get_percent(lr_passed + 1, len(lrs))})," \
                                   f" model filename = {model_filename} ({get_percent(model_passed + 1, len(model_files))})," \
                                   f" execution = {i + 1} / {exec_nb}." \
                                   f" ETA : {eta_as_string}."
                        print(general_progress, end='\r', flush=True)
                        if jordan_instance:
                            progress = to_progress(get_progress_ratio(*progress_tuples))
                            jordan_instance.send_status(general_progress)
                            jordan_instance.send_progress(progress)
                            jordan_instance.send_typed_status(status_type=STATUS_TYPE_ETA, status=eta_as_string)

                    _, _, \
                    (diversity_rate, plagia_part, rejected_for_repetition, post_processing_score) =\
                        generate(notes, instruments_index,
                                 model,
                                 generate_output_length=generate_output_length,
                                 device=device,
                                 normalized_input=normalized_input,
                                 int_to_note=int_to_note,
                                 **kwargs)
                    if jordan_instance:
                        jordan_instance.send_status(f"Diversity rate : {diversity_rate}. Plagia part : {plagia_part}. Rejected for repetition : {rejected_for_repetition}.")

                        jordan_message = jordan_instance.read_message()
                        if jordan_message:
                            if jordan_message.action_name in [SKIP_MODEL_FILE, SKIP_LEARNING_RATE, SKIP_LOSS_FUNCTION]:
                                jordan_message.acknowledge()
                                interrupt_loop = True

                    diversity_rates.append(diversity_rate)
                    plagia_parts.append(plagia_part)
                    rejected_for_repetitions.append(rejected_for_repetition)
                    post_processing_scores.append(post_processing_score)

                diversity_rate_mean = np.mean(diversity_rates)
                plagia_part_mean = np.mean(plagia_parts)
                rejected_for_repetition_mean = np.mean(rejected_for_repetitions)
                post_processing_score_mean = np.mean(post_processing_scores)
                # TODO by epoch number
                evaluation[subfolder][model_filename] = {
                    'diversity_rate': diversity_rate_mean,
                    'plagia_part': plagia_part_mean,
                    'rejected_for_repetition': rejected_for_repetition_mean,
                    'post_processing_score': post_processing_score_mean
                }

    return evaluation


def to_progress(ratio, base=100.0, as_int=True):
    progress = ratio*base
    if as_int:
        return int(progress)
    return progress



def select_models(files, select):
    if select:
        select_files = []
        for f in files:
            for s in select:
                as_model_filename = get_serialized_model_filename_by_epoch(s)
                if str(as_model_filename) in str(f):
                    select_files.append(f)
        return select_files
    else:
        return files


def get_percent(progress, total):
    return f"{100 * progress / total:.0f}%"


def extract_evaluation_feature(dic, first_key, third_key):
    """dic from evaluate_models()
    first_key is folder
    third_key is the evaluation feature, such as 'rejected_for_repetition'
    """
    extract = []
    for model_filename, model_stats in dic[first_key].items():
        extract.append(model_stats[third_key])
    return extract


def extract_epoch_from_filename(dic, first_key):
    """dic from evaluate_models()
    first_key is folder
    """
    extract = []
    for model_filename, model_stats in dic[first_key].items():
        extract.append(parse_epoch(model_filename))
    return extract


def plot_model_evaluation(evaluation, feature, **kwargs):
    plt.figure(figsize=(16, 10))
    for model_type in evaluation.keys():
        plt.plot(extract_epoch_from_filename(evaluation, model_type),
                 extract_evaluation_feature(evaluation, model_type, feature), label=model_type)
    #     plt.title(feature)
    plt.xlabel("Epoch / Model")
    plt.ylabel(feature)
    plt.legend()
    # plt.show()


def compute_evaluation_score(evaluation, features, weights):
    """adds feature 'score' to evaluation structure.
    Score is Sum(feature_value*feature_weight)
    It returns the model with best score
    """
    best_model = None
    best_score = -float('inf')
    for subfolder, model_class in evaluation.items():
        for model_filename, model_stats in model_class.items():
            epoch_trained_model_score = 0
            for ft_idx, feature in enumerate(features):
                epoch_trained_model_score += model_stats[feature] * weights[ft_idx]
            model_stats['score'] = epoch_trained_model_score
            if epoch_trained_model_score > best_score:
                best_score = epoch_trained_model_score
                best_model = subfolder + model_filename
    return best_model, best_score
