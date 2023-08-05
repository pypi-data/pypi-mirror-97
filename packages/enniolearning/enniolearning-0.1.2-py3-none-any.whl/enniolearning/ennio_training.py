from enniolearning.training_fcts import get_notes_by_instrument, prepare_sequences,get_data, train_with_losses, device
import matplotlib.pyplot as plt
from torch import nn

#Hyperparameters
hp_test_name = "classic"
hp_batch_size = 32
hp_loss_funcs = [nn.BCELoss()]
hp_nb_epochs=10
hp_learning_rates=[1e-5,1e-6]


def train(test_name=hp_test_name, nb_epochs=hp_nb_epochs, learning_rates=None, loss_funcs=None,
          notes=None, instrument_index=None, midi_files_path=None, batch_size=hp_batch_size,
          plot_result=True, jordan_instance=None, **kwargs):
    if loss_funcs is None:
        loss_funcs = hp_loss_funcs
    if learning_rates is None:
        learning_rates = hp_learning_rates
    jordan_training_task_instance = None
    if jordan_instance:
        jordan_training_task_instance = jordan_instance.create_task('training')

    if notes is None or instrument_index is None:
        if midi_files_path is None:
            midi_files_path = f"data/midi_songs/{test_name}/*.mid"
        notes, instrument_index = get_notes_by_instrument(midi_files_path=midi_files_path, **kwargs)

    lstm_input_size = len(instrument_index)
    # print(instrument_index)
    # for iN in instrument_index:
    #     iM = parse_music21_instrument(iN)
    #     print(iM, type(iM))

    network_input, network_output, note_to_int, int_to_note, sequence_length = prepare_sequences(notes, batch_size=batch_size, **kwargs)

    n_vocab = len(note_to_int)
    train_dl = get_data(network_input, network_output, batch_size, device, **kwargs)

    print('Training parameters :')
    print(f'  - Batch size : {batch_size}')
    print(f'  - sequence length : {sequence_length}. Length of each sample.')
    print(f'  - Training dataset length : {network_input.shape[0]}')
    print(f'  - Training samples count : {len(train_dl)}. (Training dataset length / Batch size)')

    if jordan_training_task_instance:
        jordan_training_task_instance.send_status(f'Starting training with Loss functions {loss_funcs}, learning rates {learning_rates} for {nb_epochs} epochs.')

    train_loss = train_with_losses(n_vocab=n_vocab, batch_size=batch_size, input_size=lstm_input_size,
                                   train_dl=train_dl, loss_funcs=loss_funcs,  epochs=nb_epochs,
                                   learning_rates=learning_rates, test_name=test_name, save_better_model=test_name,
                                   jordan_instance=jordan_training_task_instance, **kwargs)

    if jordan_training_task_instance:
        jordan_training_task_instance.send_success_status("Training complete")
        jordan_training_task_instance.complete()

    if plot_result:
        plt.figure(figsize=(18,10))
        for name,losses in train_loss.items():
            plt.plot(losses, label=name)
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        # plt.show()