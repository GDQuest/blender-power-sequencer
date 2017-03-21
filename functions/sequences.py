"""Sequence selection and editing related functions"""
import bpy
from .global_settings import SequenceTypes, SearchMode
from operator import attrgetter


def find_empty_channel(mode='ABOVE'):
    """Finds and returns the first empty channel in the VSE
    Takes the optional argument mode: 'ABOVE' or 'ANY'
    'ABOVE' finds the first empty channel above all of the other strips
    'ANY' finds the first empty channel, even if there are strips above it"""
    sequences = bpy.context.sequences

    if not sequences:
        return 1

    empty_channel = None
    channels = [s.channel for s in sequences]
    channels = sorted(list(set(channels)))

    for i in range(channels[-1]):
        if i not in channels:
            if mode == 'ANY':
                empty_channel = i
                break
    if not empty_channel:
        empty_channel = channels[-1] + 1

    return empty_channel


# TODO: refactor code - clean up / get the user to pass sequences to work on?
def find_next_sequences(mode=SearchMode.NEXT,
                        sequences=None,
                        pick_sound=False):
    """
    Returns a sequence or a list of sequences following the active one
    """
    if not sequences:
        sequences = bpy.context.sequences
        if not sequences:
            return None

    active = bpy.context.scene.sequence_editor.active_strip
    nexts = []
    nexts_far = []
    same_channel = []

    # Find all selected sequences to the right of the active sequence
    for seq in sequences:
        if (seq.frame_final_start >= active.frame_final_end) or (
                seq.frame_final_start > active.frame_final_start) & (
                    seq.frame_final_start < active.frame_final_end) & (
                        seq.frame_final_end > active.frame_final_end):
            if abs(seq.channel - active.channel) > 2:
                nexts_far.append(seq)
            elif seq.type in SequenceTypes.SOUND and not pick_sound:
                pass
            else:
                nexts.append(seq)
                if mode is SearchMode.CHANNEL and seq.channel == active.channel:
                    same_channel.append(seq)

# Store the sequences to return
    next_sequences = None
    if mode is SearchMode.CHANNEL:
        return same_channel
    elif len(nexts) > 0:
        return min(
            nexts,
            key=
            lambda next: (next.frame_final_start - active.frame_final_start))
    elif len(nexts_far) > 0:
        next_sequences = min(
            nexts_far,
            key=
            lambda next: (next.frame_final_start - active.frame_final_start))

    return next_sequences


def select_strip_handle(sequences, side=None, frame=None):
    """
    Select the left or right handles of the strips based on the frame number
    """
    if not side and sequences and frame:
        return False

    side = side.upper()

    for seq in sequences:
        seq.select_left_handle = False
        seq.select_right_handle = False

        handle_side = ''
        start, end = seq.frame_final_start, seq.frame_final_end
        if side == 'AUTO' and start <= frame <= end:
            handle_side = 'LEFT' if abs(
                frame - start) < seq.frame_final_duration / 2 else 'RIGHT'
        elif side == 'LEFT' and frame < end or side == 'RIGHT' and frame > start:
            handle_side = side
        else:
            seq.select = False
        if handle_side:
            bpy.ops.sequencer.select_handles(side=handle_side)
    return True


def mouse_select_sequences(frame=None,
                           channel=None,
                           mode='mouse',
                           select_linked=True):
    """
    Selects sequences based on the mouse position or using the time cursor
    """

    selection = []
    sequences = bpy.context.sequences
    if not sequences:
        return []

    for seq in sequences:
        channel_check = True if seq.channel == channel else False
        if channel_check and seq.frame_final_start <= frame <= seq.frame_final_end:
            selection.append(seq)
            if mode == 'mouse' or mode == 'smart' and channel_check:
                break

    if len(selection) > 0:
        # Select linked time sequences
        if select_linked and mode in ('mouse', 'smart'):
            for seq in sequences:
                if seq.channel != selection[
                        0].channel and seq.frame_final_start == selection[
                            0].frame_final_start and seq.frame_final_end == selection[
                                0].frame_final_end:
                    selection.append(seq)
    # In smart mode, if we don't get any selection, we select everything
    elif mode == 'smart':
        selection = sequences
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
        return None

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
    end = max(sequences, key=attrgetter('frame_final_end')).frame_final_end - 1

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
    if sequence.type not in SequenceTypes.VIDEO and \
       sequence.type not in SequenceTypes.IMAGE:
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
