"""Sequence selection and editing related functions"""
import bpy
from .global_settings import SearchMode


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
    # remove duplicates and sort channels
    channels = sorted(list(set(channels)))

    for i in range(channels[-1]):
        if i not in channels:
            if mode == 'ANY':
                empty_channel = i
                break
    if not empty_channel:
        empty_channel = channels[-1] + 1

    return empty_channel


def is_channel_free(target_channel, start_frame, end_frame):
    """Checks if the selected channel is empty or not. Optionally verifies that there is space in the channel in a certain timeframe"""
    # Sort sequences on screen by starting frame
    sequences = [
        s for s in bpy.context.sequences if s.channel == target_channel]

    for s in sequences:
        if start_frame <= s.frame_final_start <= end_frame or start_frame <= s.frame_final_end <= end_frame:
            return False
    return True


# TODO: refactor code - clean up / get the user to pass sequences to work on?
def find_next_sequences(mode=SearchMode.NEXT,
                        sequences=None,
                        pick_sound=False):
    """Returns a sequence or a list of sequences following the active one"""
    if not sequences:
        sequences = bpy.context.scene.sequence_editor.sequences
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
                if mode is SearchMode.CHANNEL and \
                   seq.channel == active.channel:
                    same_channel.append(seq)

    # Store the sequences to return
    next_sequences = None
    if mode is SearchMode.CHANNEL:
        return same_channel
    elif len(nexts) > 0:
        return min(
            nexts,
            key=lambda next: (next.frame_final_start - active.frame_final_start))
    elif len(nexts_far) > 0:
        next_sequences = min(nexts_far, key=lambda next: (
            next.frame_final_start - active.frame_final_start))

    return next_sequences


def select_strip_handle(sequences, side=None, frame=None):
    """Select the left or right handles of the strips based on the frame number"""
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
    """Selects sequences based on the mouse position or using the time cursor"""

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
                if seq.channel != selection[0].channel \
                   and seq.frame_final_start == selection[0].frame_final_start \
                   and seq.frame_final_end == selection[0].frame_final_end:
                    selection.append(seq)
    # In smart mode, if we don't get any selection, we select everything
    elif mode == 'smart':
        selection = sequences
    return selection
