"""Sequence selection and editing related functions"""
import bpy
from .global_settings import SequenceTypes, SearchMode
from operator import attrgetter


def get_empty_channel(sequences, mode='ABOVE'):
    """Finds and returns the first empty channel in the VSE
    Takes the optional argument mode: 'ABOVE' or 'ANY'
    'ABOVE' finds the first empty channel above all of the other strips
    'ANY' finds the first empty channel, even if there are strips above it
    """
    sequences = bpy.context.sequences
    if not sequences:
        return 1

    channels = [s.channel for s in sequences]
    channels = sorted(list(set(channels)))
    empty_channel = None

    if mode == 'ANY':
        for i in range(channels[-1]):
            if i not in channels:
                empty_channel = i
                break
    if not empty_channel:
        empty_channel = channels[-1] + 1

    return empty_channel


def find_next_sequences(sequences):
    """
    Finds the strips following the sequences passed to the function
    Args:
    - Sequences, the sequences to check
    Returns all the strips after the sequence in the current context
    """
    if not sequences:
        raise AttributeError('Missing sequences parameter')

    last_seq_start = max(sequences, key=attrgetter('frame_final_start')).frame_final_start

    next_sequences = []
    for s in bpy.context.sequences:
        if s.frame_final_start > last_seq_start:
            next_sequences.append(s)
    return next_sequences


def filter_sequences_by_type(sequences, *args):
    """
    Takes a list of sequences and returns a list of sequences with types
    that correspond to the types passed in args.
    Use the SequenceTypes class for the args

    Args:
    - sequences: a list of sequences
    - args: any list of sequence types. i.e. SequenceTypes.VIDEO
    """
    types_list = []
    for arg in args:
        if not isinstance(arg, list):
            raise TypeError('An argument is not a list')
    for arg in args:
        types_list.extend(arg)

    return [s for s in sequences if s.type in types_list]


def select_strip_handle(sequences, side=None, frame=None):
    """
    Select the left or right handles of the strips based on the frame number
    """
    if not side and sequences and frame:
        raise AttributeError('Missing attributes')

    side = side.upper()

    for s in sequences:
        s.select_left_handle = False
        s.select_right_handle = False

        handle_side = ''
        start, end = s.frame_final_start, s.frame_final_end
        if side == 'AUTO' and start <= frame <= end:
            handle_side = 'LEFT' if abs(
                frame - start) < s.frame_final_duration / 2 else 'RIGHT'
        elif side == 'LEFT' and frame < end or side == 'RIGHT' and frame > start:
            handle_side = side
        else:
            s.select = False
        if handle_side:
            bpy.ops.sequencer.select_handles(side=handle_side)
    return True


def find_strips_mouse(frame=None, channel=None, select_linked=True):
    """
    Finds a list of sequences to select based on the mouse position
    or using the time cursor.

    Args:
    - frame: the frame the mouse or cursor is on
    - channel: the channel the mouse is hovering (only used in mouse mode)
    - select_linked: include the sequences linked in time if True

    Returns the sequence(s) under the mouse cursor (can be multiple sequences
    if select_linked)
    Returns an empty list if nothing was found
    """
    sequences = bpy.context.sequences
    selection = []
    if not sequences:
        raise AttributeError('Missing sequences parameter')

    for s in sequences:
        channel_check = True if s.channel == channel else False
        if channel_check and s.frame_final_start <= frame <= s.frame_final_end:
            selection.append(s)
            break

    if select_linked and len(selection) > 0:
        for s in sequences:
            if s.channel != selection[
                    0].channel and s.frame_final_start == selection[
                        0].frame_final_start and s.frame_final_end == selection[
                            0].frame_final_end:
                selection.append(s)
    return selection


# TODO: UNITTEST: always return as many sequences as passed in
def slice_selection(sequences):
    """
    Takes a list of sequences and breaks it down
    into multiple lists of connected sequences.

    Returns a list of lists of sequences,
    each list corresponding to a block of sequences
    that are connected in time.
    """
    if not sequences:
        raise AttributeError('No sequences passed to the function')

# Find when 2 sequences are not connected in time
    sequences = sorted(sequences, key=attrgetter('frame_final_start'))

    last_sequence = sequences[0]
    break_ids = [0]
    index = 0
    for s in sequences:
        if s.frame_final_start > last_sequence.frame_final_end + 1:
            break_ids.append(index)
        last_sequence = s
        index += 1

# Create lists
    break_ids.append(len(sequences))
    cuts_count = len(break_ids) - 1
    broken_selection = []
    index = 0
    while index < cuts_count:
        temp_list = []
        index_range = range(break_ids[index], break_ids[index + 1] - 1)
        if len(index_range) == 0:
            temp_list.append(sequences[break_ids[index]])
        else:
            for counter in range(break_ids[index], break_ids[index + 1]):
                temp_list.append(sequences[counter])
        # print("SPLIT LIST: ")
        # print(str(temp_list))
        # print("\n")
        if temp_list:
            broken_selection.append(temp_list)
        index += 1
    return broken_selection


def get_frame_range(sequences=None, get_from_start=False):
    """
    Returns a tuple with the minimum and maximum frames of the
    list of passed sequences.
    If no sequences are passed, returns the timeline's start and end frames
    Args:
        - sequences, the sequences to use
        - get_from_start, the returned start frame is set to 1 if
        this boolean is True
    """
    if not sequences:
        if bpy.context.sequences:
            sequences = bpy.context.sequences
        else:
            scene = bpy.context.scene
            return scene.frame_start, scene.frame_end

    start = 1 if get_from_start else min(
        sequences, key=attrgetter('frame_final_start')).frame_final_start
    end = max(sequences, key=attrgetter('frame_final_end')).frame_final_end

    return start, end


def set_preview_range(start, end):
    """Sets the preview range and timeline render range"""
    if not (start and end) and start != 0:
        raise AttributeError('Missing start or end parameter')

    scene = bpy.context.scene

    scene.frame_start = start
    scene.frame_end = end
    scene.frame_preview_start = start
    scene.frame_preview_end = end


def find_effect_strips(sequence):
    """
    Takes a single strip and finds effect strips that use it as input
    Returns the effect strip(s) found as a list, ordered by starting frame
    Returns None if no effect was found
    """
    if sequence.type not in SequenceTypes.VIDEO and sequence.type not in SequenceTypes.IMAGE:
        return None

    effect_sequences = (s
                        for s in bpy.context.sequences
                        if s.type in SequenceTypes.EFFECT)
    found_effect_strips = []
    for s in effect_sequences:
        if s.input_1.name == sequence.name:
            found_effect_strips.append(s)
        if s.input_count == 2:
            if s.input_2.name == sequence.name:
                found_effect_strips.append(s)

    found_effect_strips = sorted(found_effect_strips,
                                 key=attrgetter('frame_final_start'))
    return found_effect_strips


def find_linked(sequences):
    """
    Takes a list of sequences and returns a list of all the sequences
    and effects that are linked to the sequences

    Args:
    - sequences: a list of sequences
    Returns a list of all the linked sequences excluding the input sequences
    """
    start, end = get_frame_range(sequences)
    sequences_in_range = [s
                          for s in bpy.context.sequences
                          if is_in_range(s, start, end)]
    effects = (s for s in sequences_in_range if s.type in SequenceTypes.EFFECT)
    selected_effects = (s for s in sequences if s.type in SequenceTypes.EFFECT)

    linked_sequences = []
    # Filter down to effects that have at least one of seq as input and
    # Append input sequences that aren't in the source list to linked_sequences
    for e in effects:
        for s in sequences:
            try:
                if e.input_2 == s:
                    linked_sequences.append(e)
                    if e.input_1 not in sequences:
                        linked_sequences.append(e.input_1)
            finally:
                if e.input_1 == s:
                    linked_sequences.append(e)
                    if e.input_2 not in sequences:
                        linked_sequences.append(e.input_2)

    # Find inputs of selected effects that are not selected
    for e in selected_effects:
        if e.input_1 not in sequences:
            linked_sequences.append(e.input_1)
        if e.input_count == 2:
            if e.input_2 not in sequences:
                linked_sequences.append(e.input_2)

    return linked_sequences


def is_in_range(sequence, start, end):
    """
    Checks if a single sequence's start or end is in the range

    Args:
    - sequence: the sequence to check for
    - start, end: the start and end frames
    Returns True if the sequence is within the range, False otherwise
    """
    s_start = sequence.frame_final_start
    s_end = sequence.frame_final_end
    return start <= s_start <= end or start <= s_end <= end