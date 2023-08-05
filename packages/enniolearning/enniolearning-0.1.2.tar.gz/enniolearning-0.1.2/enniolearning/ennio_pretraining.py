import matplotlib.pyplot as plt
from enniolearning.training_fcts import deserialize_score, deserialize_part, get_notes_by_instrument
import pickle
import random
from music21 import environment
environment.set('musescoreDirectPNGPath', 'C:\\Program Files (x86)\\MuseScore 3.5\\bin\\MuseScore3.exe')

test_name = 'The Nightmare Before Christmas'
# test_name = 'disney'
# test_name = 'frozen'
dump_path = f"../data/midi_songs/{test_name}"



notes, instrument_index = get_notes_by_instrument(f"{dump_path}/*.m*",
                                                  force_reload_dataset=True,
                                                  skip_percussion=True,
                                                  plot_raw_songs=True, plot_dataset=True,
                                                  dump_path=dump_path,
                                                  apply_part_filter=True)

# with open(f'{dump_path}/notes', 'rb') as filepath:
#     notes = pickle.load(filepath)
# with open(f'{dump_path}/instruments_index', 'rb') as filepath:
#     instrument_index = pickle.load(filepath)

print(f'{instrument_index}')

print(f'Dataset parameters :')
print(f'  These parameters matter for network size (ModelMidiLstm), and have direct impact on memory needs :')
print(f'    - Instruments count (aka lstm_input_size) : {len(instrument_index)}')
print(f'    - n_vocab (all notes counts, including pitch, quarterLength, etc.) : {len(set(note for part in notes for note in part))}')
print(f'  These parameters matter more for time than space :')
print(f'    - Training dataset length : {notes.shape[1]}')

# output_length = 70
# x = random.randint(0, notes.shape[1]-output_length-1)
# print(f"from {x} to {x+output_length}")
# mini_score = deserialize_score(notes[:,x:x+output_length], instrument_index)
# mini_score.show('midi')
# mini_score.show()

plt.show()