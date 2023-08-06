import glob
import os
import pickle
import re
import time
from fractions import Fraction
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import torch
import torch.optim as optim
from jordan_py import jordan
from music21 import *
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
import logging

from enniolearning.ennio_midi_model import ModelMidiLstm
from enniolearning.eta_tools import EtaPrinter
from enniolearning.utils import to_categorical, label_to_int, log

#https://stackoverflow.com/questions/49939275/python-music21-library-create-png-from-stream
#environment.set("musescoreDirectPNGPath", "/usr/bin/musescore")
# environment.set('musescoreDirectPNGPath', 'C:\\Program Files (x86)\\MuseScore 3.5\\bin\\MuseScore3.exe')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Jordan constants
STOP_TRAINING_LOSS_FUNC = 'Skip loss function'
STOP_TRAINING_LOSS_FUNC_LR = 'Skip learning rate'


def get_notes_by_instrument(midi_files_path="data/midi_songs/*.mid", apply_part_filter=True, dump_path='data',
                            force_reload_dataset=False, plot_raw_songs=False, plot_dataset=False, **kwargs):
    """ Get all the notes and chords from the midi files in the ./midi_songs directory
    this function returns an 2D-array of strings -> one note is one string, and all song are concatenated.
    Dimension 0 is instrument index.
    Dimension 1 is sequence of notes (strings)
    These sequences are padded (Rests) when an instrument is not active, to keep alignment (synchro between instruments).
    It also returns the list of Instruments (headers of the first dimension)."""

    if not force_reload_dataset \
            and os.path.isfile(dump_path+'/notes_by_instrument')\
            and os.path.isfile(dump_path+'/instruments_index'):

        log('Reusing serialized notes from previous parsing', **kwargs)
        with open(dump_path + '/notes_by_instrument', 'rb') as filepath:
            notes_by_instrument = pickle.load(filepath)
        with open(dump_path + '/instruments_index', 'rb') as filepath:
            instruments_index = pickle.load(filepath)

    else :
        notes_by_instrument = []
        instruments_index = []
        songs_quarterLength = []

        files_to_parse = glob.glob(midi_files_path)
        if len(files_to_parse) is 0:
            raise FileNotFoundError(f'No file to parse in {midi_files_path}. Please check [midi_files_path] key.')
        for file in files_to_parse:
            log(f"Parsing {file}", **kwargs)
            try:
                midi = converter.parse(file)
            except UnicodeDecodeError:
                log(f"Enconding error on {file}", **kwargs)
                continue

            notes_for_this_song, instruments_index = get_notes_by_instrument_for_score(midi, instruments_index, **kwargs)

            notes_by_instrument.append(notes_for_this_song)
            songs_quarterLength.append(midi.quarterLength)

        instruments_index = np.array(instruments_index)

        # 1/ ~transpose notes_by_instrument to obtain a 3D array : 1st dim = instrument, 2nd dim = song, 3rd dims = notes
        notes_by_instrument, songs_length = format_notes_to_sequence(notes_by_instrument, instruments_index, songs_quarterLength, **kwargs)

        if plot_raw_songs:
            plot_song(files_to_parse, notes_by_instrument, instruments_index, songs_length, 'Raw Dataset', **kwargs)

        # 2/ skip 2nd dim, as if dataset was a single big song
        notes_by_instrument = flatten_skip_song(notes_by_instrument)

        # 3/ filter parts from instruments already present that do not contain many notes (10% mean)
        if apply_part_filter:
            notes_by_instrument, instruments_index = filter_parts(notes_by_instrument, instruments_index, **kwargs)

        if plot_dataset:
            plot_song(files_to_parse, notes_by_instrument, instruments_index, songs_length, 'Final Dataset', **kwargs)

        with open(dump_path+'/notes_by_instrument', 'wb') as filepath:
            pickle.dump(notes_by_instrument, filepath)
        with open(dump_path+'/instruments_index', 'wb') as filepath:
            pickle.dump(instruments_index, filepath)

    return notes_by_instrument, instruments_index


def plot_song(files_to_parse, notes_by_instrument, instruments_index, songs_length, title: str = '', **kwargs):
    nb_songs = len(files_to_parse)
    is_song_dimension = notes_by_instrument.shape[1] == nb_songs
    if is_song_dimension:  # before flatten
        pitchnames = set(note for part in notes_by_instrument for song in part for note in song)
    else:  # no more song distinction, they are flattened
        pitchnames = set(note for part in notes_by_instrument for note in part)
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
    fig, ax = plt.subplots(nb_songs, num=title)
    fig.tight_layout()
    from_index = 0
    for song_index in range(nb_songs):  # by song
        ax[song_index].set_yticks(np.arange(len(instruments_index)))
        ax[song_index].set_yticklabels(instruments_index)
        ax[song_index].set_title(files_to_parse[song_index])
        if is_song_dimension:
            song_notes = notes_by_instrument[:, song_index]
        else:
            song_notes = notes_by_instrument[:, from_index:from_index+songs_length[song_index]]
            from_index = from_index + songs_length[song_index]

        ax[song_index].imshow(notes_by_instrument_as_number(song_notes, note_to_int), aspect='auto')


def notes_by_instrument_as_number(notes_by_instrument, note_to_int, **kwargs):
    return np.array([[note_to_int[notes_by_instrument[i][j]] for j in range(len(notes_by_instrument[i]))] for i in range(len(notes_by_instrument))])


def filter_parts(notes_by_instrument_detailed, instruments_index, **kwargs):
    filtered_notes_by_instrument = []
    filtered_instruments_index = []

    for instru_index_mask in group_by_same_instrument(instruments_index, **kwargs):
        indices_of_same_instrument = list(i_idx for i_idx, is_cat in enumerate(instru_index_mask) if is_cat)
        #         notes_of_macro_instrument = []
        notes_for_same_instrument, same_instruments_index = filter_algo(
            notes_by_instrument_detailed[indices_of_same_instrument], instruments_index[indices_of_same_instrument], **kwargs)

        filtered_notes_by_instrument.extend(notes_for_same_instrument)
        filtered_instruments_index.extend(same_instruments_index)

    return np.array(filtered_notes_by_instrument), np.array(filtered_instruments_index)


def filter_algo(notes_by_instrument, instruments_index, **kwargs):
    # may add several filters, one after another, with global_filter = filter1 & filter2 & filter3 (when filterX is a np.array)

    diversity_by_instru = {}

    for instru_index, notes_seq in enumerate(notes_by_instrument):
        instru_name = instruments_index[instru_index]
        unique_notes = set(notes_seq)
        diversity_by_instru[instru_name] = len(unique_notes)

    diversity_values = np.array(list(diversity_by_instru.values()))

    diversity_filter_mask = diversity_values >= min(diversity_values.max() - diversity_values.max() * 0.5,
                                                    np.quantile(diversity_values, 0.85, interpolation='higher'))

    log(
        f"Diversity filter : keep {instruments_index[diversity_filter_mask]}, reject {instruments_index[~diversity_filter_mask]}", **kwargs)

    return notes_by_instrument[diversity_filter_mask], instruments_index[diversity_filter_mask]


def group_by_same_instrument(instruments_index, **kwargs):
    """Returns boolean 2D array.
    Dimension 0 length is the category count found in the instrument catalog.
    e.g : ['Piano Right', 'Clarinet','Piano Left'] has 2 categories (Piano and Clarinet)
    Dimension 1 length == len(instrument_index). It is a boolean mask saying if the instrument in index m is of category n.
    Based on music21.instrument.fromString"""
    return (to_categorical(
        label_to_int(
            map(
                type,
                map(
                    lambda i: parse_music21_instrument(i, **kwargs), instruments_index
                )
            )
        )
    ) == 1).transpose()


def instruments_can_be_merged(instru_a, instru_b, all_parts: dict = None, **kwargs): # all_parts can be used
    if is_right_hand_name(instru_a) and is_left_hand_name(instru_b) or \
            is_right_hand_name(instru_b) and is_left_hand_name(instru_a):
        return False
    if all_parts is not None:
        if instru_a in all_parts and instru_b in all_parts:
            return False
    # should add more conditions ?
    return True


def instrument_can_be_merged_with_index(instru : str, instruments_index : list, **kwargs):
    if instru in instruments_index:
        return True, instruments_index.index(instru)
    for i in instruments_index:
        if instru in i or i in instru:
            if instruments_can_be_merged(instru, i, **kwargs):
                return True, instruments_index.index(i)
    return False, -1


def get_notes_by_instrument_for_score(score, instruments_index : list, **kwargs):
    notes_for_this_song = {}
    parts = extract_parts(score, **kwargs)
    for instru, p in parts.items():
        #         log(f'Reading notes of part {instru}', level=logging.DEBUG, **kwargs)
        can_merge, instru_index = instrument_can_be_merged_with_index(instru, instruments_index, all_parts=parts, **kwargs)
        if not can_merge:
            instruments_index.append(instru)
            instru_index = len(instruments_index) - 1

        notes_for_this_song[instru_index] = []

        # add Rests in the beginning or at the end
        if p.lowestOffset != 0.0:  # p.notesAndRests[0].offset != 0.0 :
            p.insert(0.0, note.Rest(quarterLength=p.lowestOffset))

        for element_index in range(len(p)):
            element = p[element_index]
            if isPartProperties(element):
                pass
            elif isGeneralNote(element):
                notes_for_this_song[instru_index].extend(serialize_general_note(p, element_index, **kwargs))
            else:
                log(f"Unhandled type of element in part : {type(element)}", level=logging.WARN, **kwargs)
    return notes_for_this_song, instruments_index


def format_notes_to_sequence(notes_by_instrument, instruments_index, songs_quarterLength, **kwargs):
    """
    :param songs_quarterLength: song quarterLength from music21 (not len(arrey))
    :return: notes_by_instrument as str,
    songs (notes_by_instrument.shape[1]) length in term of len() (not music21 quarterLength)
    """
    formatted_notes = []
    songs_length = []  # in term of len(), not quarterLength
    for instru_index in range(len(instruments_index)):
        instru_sequences = []
        for i, song in enumerate(notes_by_instrument):
            song_length = max(len(part) for part in song.values())
            songs_length.append(song_length)
            song_by_instru_part = pad_instru_part(song.get(instru_index, []), song_length, songs_quarterLength[i], **kwargs)
            instru_sequences.append(song_by_instru_part)
        formatted_notes.append(instru_sequences)
    return np.array(formatted_notes), songs_length


def flatten_skip_song(rearrange_notes):
    flat_notes_by_instru = []
    for instru in rearrange_notes:
        flat_notes_by_instru.append(np.hstack(list(song_notes for song_notes in instru)))
    return np.array(flat_notes_by_instru)  # type string


LEFT_HAND_CATALOG = ('LH', 'Left', 'Gauche', 'MG')
RIGHT_HAND_CATALOG = ('RH', 'Right', 'Droite', 'MD')


def skip_instru(instru_name,
                skip_percussion=False,
                skip_vocal=False,
                skip_type_list=None,
                include_type_list=None,
                skip_unsolvable=True, **kwargs):
    instru = parse_music21_instrument(instru_name, **kwargs)
    if instru is None:
        return skip_unsolvable
    if include_type_list is not None:
        for type_to_include in include_type_list:
            if isinstance(instru, type_to_include):
                return False
    if skip_percussion and isinstance(instru, instrument.Percussion):
        return True
    if skip_vocal and isinstance(instru, instrument.Vocalist):
        return True
    if skip_type_list is not None:
        for type_to_skip in skip_type_list:
            if isinstance(instru, type_to_skip):
                return True
    return False


def extract_parts(score, **kwargs):
    """Return a dict key=detailed-instrument (e.g Piano Left-Hand), value=collection of simultaneous streams"""
    """Voices level handled"""

    parts_by_instru = {}
    instruments_in_score = []

    for p in score.parts:
        if hasVoice(p):  # (contains stream.Voice)
            voice_index = 0
            for v in p.voices:
                # TODO add Rest if offset != 0
                instru = extract_details_on_instrument(p, v, history=instruments_in_score, **kwargs)
                if not skip_instru(instru, **kwargs):
                    voice_title = instru + ((' V' + str(voice_index)) if len(p.voices) > 1 else '')
                    parts_by_instru[voice_title] = v
                    voice_index += 1
        else:
            instru = extract_details_on_instrument(p, history=instruments_in_score, **kwargs)
            if not skip_instru(instru, **kwargs):
                parts_by_instru[instru] = p.recurse(classFilter=note.GeneralNote)

    return parts_by_instru


def hasVoice(part):
    return len(part.voices) is not 0


def deserialize_score(serialized_score, instruments_index, **kwargs):
    score = stream.Score()
    for instru_index, instrument_name in enumerate(instruments_index):
        p = deserialize_part(serialized_score[instru_index], **kwargs)
        p.partName = instrument_name
        p.insert(0, parse_music21_instrument(instrument_name, **kwargs))
        score.append(p)
    return score


def deserialize_part(serialized_part, **kwargs):
    """Input : array of serialized general notes"""
    part = stream.Part()

    # create note and chord objects based on the values generated by the model
    for pattern in serialized_part:
        new_note = deserialize_general_note(pattern, **kwargs)
        if new_note is not None:
            part.append(new_note)
    return part


def deserialize_general_note(pattern, **kwargs):
    # TEMPORARY WORKAROUND
    if pattern == 'R_4.0':
        return padding_note(padding_rest_quarter_length=1)
    # END OF TEMPORARY WORKAROUND
    # handle Padding
    if pattern == PADDING_STR: #warning : pattern is of type numpy.str_
        return padding_note(**kwargs)
    note_and_length = pattern.split('_')
    if len(note_and_length) is 2:
        general_note = deserialize_note(note_and_length[0])
        quarter_length = extract_quarter_length(note_and_length[1], **kwargs)
        general_note.quarterLength = quarter_length
        return general_note
    else:
        log(f"Unhandled deserialization for note {pattern}", level=logging.ERROR, **kwargs)
        return None


def padding_note(padding_rest_quarter_length=1, **kwargs):
    padding = note.Rest()
    padding.quarterLength = padding_rest_quarter_length
    return padding


def deserialize_note(pattern):
    """note/pitch/chord with octave or rest"""
    if pattern is 'R':
        return note.Rest()
    pitches = pattern.split('.')

    try:
        return chord.Chord(pitches)
    except:
        # octave -1 is confused with bemol/flat notes
        # in particular, F#-1 (octave -1) is not created because #(sharp) + -(flat) is not compatible
        return note.Rest()
    # OFFSET ?


def extract_quarter_length(pattern, min_length=1/3, **kwargs):
    if float(pattern) <= 0.0:
        log("cheating on note quarter length", level=logging.WARN, **kwargs)
        return Fraction(min_length)
    # can be a decimal (e.g 0.5) or a fraction (e.g 1/3)
    return Fraction(pattern)


def isGeneralNote(element):
    return isinstance(element, note.GeneralNote)


def isPartProperties(element):
    return isinstance(element, (instrument.Instrument, tempo.MetronomeMark, key.Key, meter.TimeSignature))


def serialize_general_note(s, element_index=0, split_long_note=True, min_length=1/3,
                           max_length_note=4.0, max_length_rest=2.0, **kwargs):
    """Input : Stream, index of current element
        Output : an array of serialized notes. Generally, this array contains a single serialized note.
        But if this note had to be split (this is often the case for rests),
        many notes of max length max_length are returned.
        Consequently, extend() function can be used to 'append all' these serialized notes.
    """
    element = s[element_index]
    max_length = max_length_rest if isinstance(element, note.Rest) else max_length_note

    note_length = extract_length(s, element_index, **kwargs)
    pitch_as_str = serialize_pitch(element, **kwargs)

    # work by measure here
    # instead of having a very long note/rest, add many notes/rests, each having max quarterLength=4
    array_of_serialized_notes = []
    if pitch_as_str is not None:
        if split_long_note and note_length/max_length > 1.0:
            nb_max_length_notes = int(note_length / max_length)
            for i in range(nb_max_length_notes):
                array_of_serialized_notes.append(as_serialized_note(pitch_as_str, max_length, min_length=min_length, **kwargs))
            surplus = note_length % max_length
            if surplus >= min_length:
                array_of_serialized_notes.append(as_serialized_note(pitch_as_str, surplus, min_length=min_length, **kwargs))
        else:
            array_of_serialized_notes.append(as_serialized_note(pitch_as_str, note_length, min_length=min_length, **kwargs))

    return array_of_serialized_notes


def as_serialized_note(pitch_str, length, **kwargs):
    return pitch_str + '_' + str(length_rounding(length, **kwargs))


def serialize_pitch(element, **kwargs):
    if isinstance(element, note.Note):
        return str(element.nameWithOctave)
    elif isinstance(element, chord.Chord):
        return '.'.join(serialize_pitch(p, **kwargs) for p in element.pitches)
    elif isinstance(element, note.Rest):
        return 'R'
    elif isinstance(element, pitch.Pitch):
        return str(element.nameWithOctave)
    else:
        log(f"Unhandled type of Note in part : {type(element)}", level=logging.ERROR, **kwargs)
        return None


def extract_length(s, element_index, **kwargs):
    """Input : Stream, index of current element
    It is sometimes not true...
    rounding : False or value for quarter rounding. Defaults to 0.5 quarter
    """
    # str(s[element_index].quarterLength) has issue with Rests...
    if element_index == len(s) - 1:
        # last element
        length = s[element_index].quarterLength
    # otherwise, substract offset
    else:
        length = s[element_index + 1].offset - s[element_index].offset
        if length <= 0.0:
            length = s[element_index].quarterLength

    length = length_rounding(length, **kwargs)

    return length


def length_rounding(length, rounding=0.5, min_length=1/3, **kwargs):
    rounded_length = length
    if rounding:
        rounded_length = length - (length % rounding)

    if min_length and rounded_length < min_length:
        rounded_length = min_length

    return rounded_length


def default_instrument(default_music21_instrument=None, **kwargs):
    return default_music21_instrument if default_music21_instrument is not None else instrument.Piano()


def extract_details_on_instrument(p, voice=None, history=[], **kwargs):
    """Returns a name (=string) for this track (part*voice).
    It is the instrument name, plus an optional detail (such as left/right hand), incremented if necessary (e.g Violin, Violin 2, Violin 3)
    """
    # 1/ try from partName
    instru_from_partname = parse_music21_instrument(p.partName, **kwargs)

    # 2/ get instrument of voice (if any)
    instrumentname_from_voice = extract_single_instrument(
        voice.getInstruments(recurse=False), **kwargs) if voice is not None else None

    # 3/ get instrument from stream.Part
    part_instrus = p.getInstruments(recurse=False)
    if has_several_instruments(part_instrus) and voice is not None:
        # sometimes, one part has several instruments (as it contains several voices)
        instrumentname_from_part = part_voice_instru_matching(p, voice, part_instrus)
    else:
        instrumentname_from_part = extract_single_instrument(part_instrus, **kwargs)

    instru = best_instrument(instru_from_partname, instrumentname_from_voice, instrumentname_from_part, **kwargs)

    if instru is None:
        instru = default_instrument(**kwargs)

    if has_hands(instru):
        guess_hand(instru, p, voice)

    instru_name = instru.instrumentName
    instru_name = normalize_hand(instru_name)

    if instru_name in history:
        instru_name = increment_instru_name(instru_name, 2, history)
    history.append(instru_name)
    #     log(f"instru_name {type(instru_name)}", level=logging.DEBUG, **kwargs)
    return instru_name


def instrument_from_string(instru):
    """instrument.fromString fails for some instruments. here is the backup for known failures."""
    mapping = {
        'guitar': instrument.Guitar,
        'flute': instrument.Flute,
        'organ': instrument.Organ,
        'synth': instrument.ElectricOrgan,
        'alto': instrument.Viola,
        'orgue': instrument.PipeOrgan,
        'church org': instrument.PipeOrgan,
        'corde': instrument.StringInstrument,
        'string': instrument.StringInstrument,
    }
    for k in mapping.keys():
        if k in instru.lower():  # is is ok ? what if composed names ? e.g electric guitar
            return mapping[k]()
    return None


def parse_music21_instrument(instru, **kwargs):
    if instru is None:
        return None
    if isinstance(instru, instrument.Instrument):
        return instru
    instru = str(instru)
    if instru is None or len(instru) == 0:
        return default_instrument(**kwargs)
    try:
        match = instrument.fromString(instru)
    except exceptions21.InstrumentException:
        # try if exact name exists in the 'music21.instrument' module
        if instru in instrument.__dict__.keys():
            match = instrument.__dict__[instru]()
        else:
            match = instrument_from_string(instru)
    return match if match is not None else default_instrument(**kwargs)


def is_super_type_of_one_element(test_super_type: type, list_of_types: list):
    for t in list_of_types:
        if is_super_type_of(test_super_type(), t()):
            return True
    return False


def best_instrument_type(types, preferred_instruments: list = None, **kwargs):
    """
    Algo : (1) from preferred_instruments if any.
     (2) from instrument class inheritance.
     (3) from instrument.classSet depth
     (4) from alphabetical order of instrument type (name), to avoid random pick
    :param types: concurrent types (not unique) from which select the best
    :param preferred_instruments: list of types (e.g [instrument.Piano, instrument.Viola]), ordered by preference
    :param kwargs:
    :return: the best type, (as a type, not an instance)
    """
    if preferred_instruments is None:
        preferred_instruments = []
    # (1)
    for preference in preferred_instruments:
        if preference in types:
            return preference

    # (2)
    sub_types = [i for i in types if not is_super_type_of_one_element(i, types)]
    if len(set(map(str, sub_types))) == 1:  # if single kind of type, return first (all same)
        return sub_types[0]

    # (3)
    max_depth = 0
    deeper = ()
    for instru_type in sub_types:
        depth = len(instru_type().classSet)
        if depth == max_depth:
            deeper = instru_type, *deeper
        if depth > max_depth:
            deeper = instru_type,  # as a tuple
            max_depth = depth
    if len(deeper):
        return deeper[0]

    # (4)
    return sorted(deeper, key=str)[0]


def best_instrument_name(instru: instrument.Instrument, instrument_guesses, **kwargs):
    kept_names = set(extract_name_of_instru(i, **kwargs) for i in instrument_guesses if should_keep_instrument_name(i, **kwargs))
    if len(kept_names) > 0:
        return ' ,'.join(kept_names)
    return None


def best_instrument(*guesses, **kwargs):
    guesses = list(filter(lambda g : g is not None, guesses))
    instrument_guesses = list(filter(lambda t: isinstance(t, instrument.Instrument),
                                     map(lambda g: parse_music21_instrument(g, **kwargs), guesses)))
    types = list(map(type, instrument_guesses))
    unique_types_str = set(map(str, types))
    if len(unique_types_str) == 0 or len(types) == 0:
        return None
    # whether we have one or several instrument, pick one, and set information as the instrumentName
    if len(unique_types_str) == 1:
        best_candidate = types[0]()
    else:
        best_candidate = best_instrument_type(types, **kwargs)()
    better_name = best_instrument_name(best_candidate, instrument_guesses, **kwargs)
    if better_name:
        best_candidate.instrumentName = better_name
    #     log(f"best candidate : {best_candidate.instrumentName} of type {type(best_candidate)} from {guesses}", level=logging.DEBUG, **kwargs)
    return best_candidate


def part_voice_instru_matching(p, v, instru_stream):
    """This is some quite poor algorithm. Wondering how MuseScore makes fine matching whereas music21 parsing is quite poor"""
    voice_index = get_voice_index(v, p)
    matching_index = voice_index % len(instru_stream)
    for i in range(matching_index, len(instru_stream)):
        if instru_stream[i].instrumentName is not None and instru_stream[i].instrumentName is not '':
            return instru_stream[i].instrumentName


def get_voice_index(voice, part):
    """Kind of part.index(voice) but only for Voices. Parts usually has other elements in the beginning (Clef, TimeSignature, etc.)"""
    index = 0
    for v in part.voices:
        if voice is v:
            return index
        index += 1


def extract_single_instrument(instru_stream, **kwargs):
    for i in reversed(instru_stream):
        extracted = extract_name_of_instru(i, **kwargs)
        if extracted is not None:
            return extracted
    return None


def extract_name_of_instru(instru, **kwargs):
    if instru is None:
        return None
    if isinstance(instru, str):
        return instru
    if isinstance(instru, instrument.Instrument):
        if instru.instrumentName is not None and instru.instrumentName is not '':
            if should_keep_instrument_name(instru, **kwargs):
                return instru.instrumentName
        return instru.classes[0]  # this returns a str
    return None


def is_sub_type_of(sub_type_instance: instrument.Instrument, super_type_instance: instrument.Instrument):
    return isinstance(sub_type_instance, type(super_type_instance)) \
            and not isinstance(super_type_instance, type(sub_type_instance))


def is_super_type_of(super_type_instance: instrument.Instrument, sub_type_instance: instrument.Instrument):
    return is_sub_type_of(sub_type_instance, super_type_instance)


def should_keep_instrument_name(instru: instrument.Instrument, **kwargs):
    # instrument name has more information than instrument type.
    instru_instance_from_instrument_name = parse_music21_instrument(instru.instrumentName, **kwargs)
    if is_sub_type_of(instru_instance_from_instrument_name, instru):
        return True
    instru_instance_from_part_name = parse_music21_instrument(instru.partName, **kwargs)
    if is_sub_type_of(instru_instance_from_part_name, instru):
        return True
    return contains_one_of(instru.instrumentName, LEFT_HAND_CATALOG) \
           or contains_one_of(instru.instrumentName, RIGHT_HAND_CATALOG) \
           or contains_one_of(instru.partName, LEFT_HAND_CATALOG) \
           or contains_one_of(instru.partName, RIGHT_HAND_CATALOG)


def has_several_instruments(instru_stream):
    return len(
        np.unique(
            list(
                filter(
                    lambda instru_name: instru_name is not None and instru_name is not '',
                    map(
                        lambda instru: instru.instrumentName,
                        instru_stream
                    )
                )
            )
        )
    ) > 1


def has_hands(instru):
    return type(instru) in [instrument.Piano]


def normalize_hand(instru):
    instru = str(instru).replace('Left Hand', 'LH')
    instru = str(instru).replace('Left', 'LH')
    instru = str(instru).replace('Right Hand', 'RH')
    instru = str(instru).replace('Right', 'RH')
    return instru


def guess_hand(instru, p, v):
    """returns the instrument name for the part/voice added with the hand, if guessable"""
    hand = ''
    #     if ~ isHandInInstrumentName(instru):
    if is_left_hand_part(p, v):
        hand = ' LH'
    elif is_right_hand_part(p, v):
        hand = ' RH'
    instru.instrumentName += hand


# def isHandInInstrumentName(instru):
#     if instru.instrumentName is not None:
#         return containsOneOf(instru.instrumentName, LEFT_HAND_CATALOG + RIGHT_HAND_CATALOG)

def is_left_hand_part(p, v):
    return is_left_hand_name(p.partName) or is_clef_type(v if v is not None else p, clef.BassClef)


def is_left_hand_name(name):
    return contains_one_of(name, LEFT_HAND_CATALOG)


def is_right_hand_name(name):
    return contains_one_of(name, RIGHT_HAND_CATALOG)


def is_right_hand_part(p, v):
    return is_right_hand_name(p.partName) or is_clef_type(v if v is not None else p, clef.TrebleClef)


def contains_one_of(name, tries):
    for word in tries:
        if str(word).lower() in str(name).lower():
            return True
    return False


def is_clef_type(s, clefType):
    return type(clef.bestClef(s.flat)) is clefType


def increment_instru_name(instruName, incr, keep_track):
    if incremented_instru_name(instruName, incr) not in keep_track:
        return incremented_instru_name(instruName, incr)
    return increment_instru_name(instruName, incr + 1, keep_track)


def incremented_instru_name(instruName, incr):
    return instruName + ' - ' + str(incr)


def create_network(n_vocab=None, batch_size=None, device=device, input_size=1, **kwargs):
    """ create the structure of the neural network """
    if not n_vocab or not batch_size:
        raise KeyError('Provide at least batch_size and n_vocab to create_network')
    model = ModelMidiLstm(n_vocab, input_size, **kwargs)
    #     model = SimpleModelMidiLstm(n_vocab, input_size=1, lstm_hidden_cells_count=256, lstm_layer_count = 3)
    model.to(device)
    model.init_state(batch_size)

    return model


def load_network(model=None, batch_size=1, device=device, weight_file=None, **kwargs):
    if model is None and weight_file is None:
        raise KeyError('Provide at least one of (model, weight_file)')

    if isinstance(model, nn.Module):
        model.to(device)
        model.init_state(batch_size)
    else:
        if weight_file is None:
            weight_file = model

        model = create_network(batch_size=batch_size, device=device, **kwargs)

        if weight_file is not None:
            log(f'Loading weight from {weight_file}', **kwargs)
            if type(weight_file) is str:
                model.load_state_dict(torch.load(weight_file))
    return model


def resume_or_create_model(resume_model=None, lr=None, test_name=None, **kwargs):
    if resume_model is not None:
        if type(resume_model) is int and lr and test_name:
            filename = get_serialized_model_name_by_epoch(make_path(test_name, f"{lr:.0E}"), resume_model)
        elif type(resume_model) is str:
            filename = resume_model
        else:
            raise KeyError(f'resume model {resume_model} of type {type(resume_model)} is not supported to resume training from it')
        log(f"Resuming model from filename {filename}", **kwargs)
        model = load_network(filename, **kwargs)
    else:
        model = create_network(**kwargs)
    return model


def reuse_network(model, batch_size=1, **kwargs):
    if type(model) is ModelMidiLstm \
            and hasattr(model, 'hidden') \
            and len(model.hidden) == 2 \
            and model.hidden[0].shape[1] == batch_size \
            and model.hidden[1].shape[1] == batch_size:
        return model
    return load_network(model, batch_size, **kwargs)


def epoch_time(start_time, end_time):
    elapsed_time = end_time - start_time
    elapsed_hours = int(elapsed_time / 3600)
    elapsed_mins = int(elapsed_time / 60 - elapsed_hours * 60)
    elapsed_secs = int(elapsed_time - elapsed_hours * 3600 - elapsed_mins * 60)
    return elapsed_hours, elapsed_mins, elapsed_secs


def loss_batch(model, criterion, batch_input, batch_target, opt=None, **kwargs):
    if opt is not None:
        opt.zero_grad()

    #     log(f"input : {xb.shape}", level=logging.DEBUG)
    predictions = model(batch_input)
    #     log(f"Computing loss between", level=logging.DEBUG, **kwargs)
    #     log(f"output : {predictions.shape}", level=logging.DEBUG, **kwargs)
    #     log(f"target : {batch_target.shape}", level=logging.DEBUG, **kwargs)
    #     predictions[some_batch] is 2D tensor, len=158=n_vocab. probabilities of the next note/pitch
    #     batch_target[some_batch] is 1D tensor, len=158=n_vocab. one 1, n_vocab-1 0 -> next note/pitch target
    loss = criterion(predictions, batch_target.float())

    if opt is not None:
        #         opt.zero_grad()
        loss.backward()
        opt.step()

    return loss.item()  ##before backward ???


def fit(model, loss_func, opt, batch_size, epochs=50, train_dl=None, print_epoch_count=10, save_better_model=False,
        progress_base=0, progress_rate=1.0, eta_printer=None, jordan_instance=None, **kwargs):
    if train_dl is None:
        train_dl = []
    train_loss = []
    start_time = time.time()
    best_loss = 100000.0
    jordan_message, interrupt_loop = None, False
    for epoch in range(epochs):
        # jordan loop control
        if interrupt_loop:
            if jordan_message and jordan_message.action_name == STOP_TRAINING_LOSS_FUNC_LR:
                jordan_message.processed()
            break

        # TRAIN MODE
        epoch_loss = 0.0
        model.train()
        #         model.zero_grad() #right ????
        for xb, yb in train_dl:
            #             log(f"xb shape : {xb.shape}", level=logging.DEBUG, **kwargs)  # (batch_size, time_sequence_length, 1 note/pitch)
            #             log(f"yb shape : {yb.shape}", level=logging.DEBUG, **kwargs)  # (batch_size, n_vocab)
            loss = loss_batch(model, loss_func, xb, yb, opt, **kwargs)
            epoch_loss += loss

        epoch_loss_train = epoch_loss / len(train_dl)
        train_loss.append(epoch_loss_train)

        model.eval()  # useless ?

        if epoch_loss_train < best_loss and save_better_model:
            save_model(save_better_model, epoch, model)
            best_loss = epoch_loss_train

        if print_periodically(epoch, epochs, print_epoch_count, **kwargs):
            end_time = time.time()
            epoch_hrs, epoch_mins, epoch_secs = epoch_time(start_time, end_time)
            epoch_status = f'Epoch: {epoch + 1:02} | Epoch Time: {epoch_hrs}h {epoch_mins}m {epoch_secs}s'
            train_loss_status = f'\tTrain Loss: {epoch_loss_train:.5f}'
            log(epoch_status, **kwargs)
            log(train_loss_status, **kwargs)
            if jordan_instance:
                jordan_instance.send_status(epoch_status + train_loss_status)

        if jordan_instance:
            jordan_instance.send_typed_status('training_loss', f"{epoch} : {epoch_loss_train}")
            jordan_instance.send_progress(progress_base + int(100 * progress_rate * (epoch+1)/epochs))
            jordan_instance.send_typed_status('eta', f"{eta_printer.print_eta((epoch, epochs))}")
            jordan_message = jordan_instance.read_message()
            if jordan_message:
                if jordan_message.action_name == STOP_TRAINING_LOSS_FUNC_LR or jordan_message.action_name == STOP_TRAINING_LOSS_FUNC:
                    jordan_message.acknowledge()
                    interrupt_loop = True

        model.reinit_state(batch_size)

    return train_loss, jordan_message


def print_periodically(current_step, max_step, printing_count, **kwargs):
    # print last step
    if(current_step is max_step -1) or (max_step <= printing_count):
        return True
    return current_step % (max_step // printing_count) == 0


DEFAULT_SAVE_FOLDER = "../save_state/"
MODEL_FILE_PREFIX = "lstm-epoch-"


def save_model(path_str, epoch, model, save_folder_root=DEFAULT_SAVE_FOLDER, **kwargs):
    """Path as string (use make_path())
    """
    Path(save_folder_root, path_str).mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), get_serialized_model_name_by_epoch(path_str, epoch))


def get_serialized_model_name_by_epoch(subfolder, epoch, save_folder_root=DEFAULT_SAVE_FOLDER, **kwargs):
    return save_folder_root + subfolder + get_serialized_model_filename_by_epoch(epoch)


def get_serialized_model_filename_by_epoch(epoch):
    return MODEL_FILE_PREFIX + f"{int(epoch):03}"


def get_serialized_model_name_by_filename(subfolder, filename, save_folder_root=DEFAULT_SAVE_FOLDER, **kwargs):
    return save_folder_root + subfolder + filename


def parse_epoch(filename, **kwargs):
    regex = ".*" + MODEL_FILE_PREFIX + "([0-9]{3})"
    try:
        parsed = re.search(regex, filename)
        if parsed and parsed.group(1):
            return int(parsed.group(1))
    except:
        log(f"parsing error on filename {filename}", level=logging.FATAL, **kwargs)
    return filename


def make_path(*folders):
    """folders : tuple or list of subsequent folders.
    Returns them separated by separator ('/')
    """
    # separator = os.sep
    separator = '/'
    return separator.join(folders) + separator


def list_model_files(subfolder, **kwargs):
    try:
        return os.listdir(DEFAULT_SAVE_FOLDER + subfolder)
    except FileNotFoundError as fnf:
        log(f'File not found {str(fnf)}', level=logging.ERROR, **kwargs)
        return []


PADDING_STR = str(0)


def pad_instru_part(notes_seq, size, quarterLength, **kwargs):
    if len(notes_seq) == 0:
        # this instrument is not in this song. fill with rests
        ignore_this_instru = stream.Stream()
        ignore_by_rest = note.Rest(quarterLength=quarterLength)
        ignore_this_instru.append(ignore_by_rest)
        notes_seq.extend(serialize_general_note(ignore_this_instru, **kwargs))
    if len(notes_seq) >= size:
        return notes_seq

    log('*** IMPROVE THIS ? *** because we may loose time and synchronization between instruments here', level=logging.DEBUG, **kwargs)
    padding = np.full(size - len(notes_seq), PADDING_STR)
    return np.hstack((notes_seq, padding))


def split_sequences(notes_by_instru, sequence_length, note_to_int, **kwargs):
    network_input = []
    network_output = []
    for notes in notes_by_instru:
        network_input_by_instru = []
        network_output_by_instru = []
        for i in range(0, len(notes) - sequence_length, 1):
            sequence_in = notes[i:i + sequence_length]
            sequence_out = notes[i + sequence_length]
            network_input_by_instru.append([note_to_int[char] for char in sequence_in])
            network_output_by_instru.append(note_to_int[sequence_out])
        network_input.append(network_input_by_instru)
        network_output.append(network_output_by_instru)

    return np.array(network_input), np.array(network_output)  # type int


MIN_SEQ_LENGTH = 100


def compute_sequence_length(batch_size, full_sample_length):
    for test_seq_len in range(MIN_SEQ_LENGTH, MIN_SEQ_LENGTH + batch_size):
        if ((full_sample_length - test_seq_len) % batch_size) == 0:
            return test_seq_len


def prepare_sequences(notes_by_instrument, sequence_length=None, batch_size=32, predict_mode=False,
                      dump_path='data', force_reload_dataset=False, **kwargs):
    reuse_dump_files = not force_reload_dataset \
                       and os.path.isfile(dump_path + '/network_input') \
                       and os.path.isfile(dump_path + '/network_output') \
                       and os.path.isfile(dump_path + '/note_to_int')\
                       and os.path.isfile(dump_path + '/int_to_note')
    if reuse_dump_files:
        with open(dump_path + '/network_input', 'rb') as filepath:
            network_input = pickle.load(filepath)
        with open(dump_path + '/network_output', 'rb') as filepath:
            network_output = pickle.load(filepath)
        with open(dump_path + '/note_to_int', 'rb') as filepath:
            note_to_int = pickle.load(filepath)
        with open(dump_path + '/int_to_note', 'rb') as filepath:
            int_to_note = pickle.load(filepath)

    else:
        pitchnames = set(note for part in notes_by_instrument for note in part)
        note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
        int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

        # cut into pieces of length=sequence_length. A bunch of sequences will form a batch.
        # That's why sequence_length should be batch_size-dependent (so only full batches are given to the model-training)

        # network_input.shape[1] should be a multiple of batch_size. adujst sequence_length to obtain it, because all batches should be full (all the same count of elements
        if sequence_length is None:
            sequence_length = compute_sequence_length(batch_size, notes_by_instrument.shape[1])

        network_input, network_output = split_sequences(notes_by_instrument, sequence_length, note_to_int, **kwargs)

        # transpose to get instrument (1st) dimension in last position, as batch will be splitted from first dimension with DataLoader
        network_input = network_input.transpose(1, 2, 0)
        network_output = network_output.transpose()

    # normalize input
    n_vocab = len(note_to_int)
    normalized_input = network_input / float(n_vocab)

    if (predict_mode):
        # reshape the input into a format compatible with LSTM layers
        return network_input, normalized_input, note_to_int, int_to_note, sequence_length
    else:
        if not reuse_dump_files:
            with open(dump_path+'/network_input', 'wb') as filepath:
                pickle.dump(network_input, filepath)
            with open(dump_path+'/network_output', 'wb') as filepath:
                pickle.dump(network_output, filepath)
            with open(dump_path+'/note_to_int', 'wb') as filepath:
                pickle.dump(note_to_int, filepath)
            with open(dump_path+'/int_to_note', 'wb') as filepath:
                pickle.dump(int_to_note, filepath)
        network_output = to_categorical(network_output, len(note_to_int))

        return normalized_input, network_output, note_to_int, int_to_note, sequence_length


def to_tensor(nparray, device=device):
    #as toch tensor
    tensor = torch.tensor(nparray)
    tensor = tensor.float().to(device)
    return tensor


def get_data(x_train, y_train, bs, device, **kwargs):
    train_ds = TensorDataset(to_tensor(x_train, device), to_tensor(y_train, device))
    return DataLoader(train_ds, batch_size=bs, shuffle=True)


def train_with_losses(loss_funcs=None, learning_rates=None,
                      save_better_model=False, jordan_instance=None, **kwargs):
    """save_better_model : False or the name of the training (will be the subroot folder name)
    """
    if learning_rates is None:
        learning_rates = [1e-3]
    if loss_funcs is None:
        loss_funcs = [nn.BCELoss()]
    train_loss = {}
    # global_eta = EtaPrinter()
    if jordan_instance:
        jordan_instance.send_status(f"About to train with {loss_funcs} loss function(s) and {learning_rates} learning rate(s) -> {len(loss_funcs) * len(learning_rates)} child task(s)")

    for loss_func in loss_funcs:

        interrupt_loop_skip_to_next_loss_func, loss_func_jordan_message = False, None
        for ilr, lr in enumerate(learning_rates):
            # jordan loop control
            if interrupt_loop_skip_to_next_loss_func:
                if loss_func_jordan_message:
                    loss_func_jordan_message.processed()
                break

            jordan_loss_function_lr_task = None
            if jordan_instance:
                loss_func_actions = jordan.with_action(STOP_TRAINING_LOSS_FUNC).with_action(
                    STOP_TRAINING_LOSS_FUNC_LR).build()
                jordan_loss_function_lr_task = jordan_instance.create_task(task_name=f"training with {loss_func} {lr}",
                                                                        actions=loss_func_actions)

            progress_base = int(100 * ilr / len(learning_rates))
            progress_rate = 1 / len(learning_rates)
            if jordan_loss_function_lr_task:
                jordan_loss_function_lr_task.send_progress(progress_base)
            lr_eta = EtaPrinter()

            model = resume_or_create_model(lr=lr, **kwargs)
            opt = optim.RMSprop(model.parameters(), lr=lr)
            loss_func = loss_func.to(device)

            start_training_msg = f"Train model with loss {loss_func} with learning rate {lr}"
            log(start_training_msg, **kwargs)
            if jordan_instance:
                jordan_instance.send_status(start_training_msg)
                if jordan_loss_function_lr_task:
                    jordan_loss_function_lr_task.send_status(start_training_msg)

            if save_better_model:
                if len(loss_funcs) > 1:
                    # if len(learning_rates) > 1: #do not skip lr level. loss function may be skipped. Check make_path(test_name, LEARNING_RATE) in ennio_models_evaluation.evaluate() if behavior is changed.
                    subfolder = make_path(save_better_model, loss_func, f"{lr:.0E}")
                    # else:
                    #     subfolder = make_path(save_better_model, loss_func)
                else:
                    # if len(learning_rates) > 1:
                    subfolder = make_path(save_better_model, f"{lr:.0E}")
                    # else:
                    #     subfolder = make_path(save_better_model)
            else:
                subfolder = save_better_model

            #             try:
            train_loss[str(loss_func) + str(lr)], loss_func_jordan_message = fit(model, loss_func, opt,
                                                                                 save_better_model=subfolder,
                                                                                 progress_base=progress_base,
                                                                                 progress_rate=progress_rate,
                                                                                 eta_printer=lr_eta,
                                                                                 jordan_instance=jordan_loss_function_lr_task,
                                                                                 **kwargs)

            if loss_func_jordan_message:
                if loss_func_jordan_message.action_name == STOP_TRAINING_LOSS_FUNC:
                    loss_func_jordan_message.acknowledge()
                    interrupt_loop_skip_to_next_loss_func = True

            if jordan_loss_function_lr_task:
                jordan_loss_function_lr_task.complete()

    return train_loss