from enniolearning.prediction_fcts import generate
from enniolearning.training_fcts import device, get_serialized_model_name_by_epoch, make_path
import pickle
from time import time

start_time = time()

#BY FILENAME

#Parameters
generate_output_length=50
test_name = 'The Nightmare Before Christmas'
lr=1e-5
epoch=289



dump_path = f"../data/midi_songs/{test_name}"
# loss_func_name = loss_func
filename = get_serialized_model_name_by_epoch(make_path(test_name, f"{lr:.0E}"), epoch)
#filename = get_serialized_model_name_by_epoch(make_path("final-fantasy-102","1E-03"), 83)

with open(f'{dump_path}/network_input', 'rb') as filepath:
    ni = pickle.load(filepath)
with open(f'{dump_path}/note_to_int', 'rb') as filepath:
    nti = pickle.load(filepath)
with open(f'{dump_path}/int_to_note', 'rb') as filepath:
    itn = pickle.load(filepath)


output_filename, prediction_output_as_int, \
(diversity_rate, plagia_part, rejected_for_repetition, post_processing_score) = \
    generate(model=filename, lstm_hidden_cells_count=256,
             generate_output_length=generate_output_length,
             device=device,
             plot_diversity=False,
             # serialize_prediction=f"../generated/{test_name}/{int(time())}",
             create_midi_file=True,
             start_playback=True,
             enable_evaluation=False,
             enable_post_processing=True,
             network_input=ni, int_to_note=itn, note_to_int=nti,
             dump_path=dump_path)
# score = converter.parse(output_filename)

print("diversity :", f"{diversity_rate*100:01.2f}%",
      "\t plagia part :", plagia_part, "/", generate_output_length,
      "\t rejected?", rejected_for_repetition,
      "\t post-processing score", post_processing_score)
if output_filename:
    print(f"{output_filename} file created !")
#make a model to classify if it is acceptable from 1- diversity, repetitions, and generated part
#don't accept 0% generatd (exactly the same as dataset part)

end_time = time()
print(f"prediction took {int(end_time-start_time)} secs")
