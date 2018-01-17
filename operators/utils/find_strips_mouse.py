import bpy

def find_strips_mouse(frame=None, channel=None, select_linked=True):
    """
    Finds a list of sequences to select based on the mouse position
    or using the time cursor.

    Args:
    - frame: the frame the mouse or cursor is on
    - channel: the channel the mouse is hovering
    - select_linked: include the sequences linked in time if True

    Returns the sequence(s) under the mouse cursor as a list
    Returns an empty list if nothing found
    """
    sequences = bpy.context.sequences
    selection = []

    for s in sequences:
        if s.lock or (not s.channel == channel):
            continue
        if s.frame_final_start <= frame <= s.frame_final_end:
            selection.append(s)
            break

    if select_linked and len(selection) > 0:
        for s in sequences:
            if s.channel == selection[0].channel or s.lock:
                continue
            if s.frame_final_start == selection[0].frame_final_start and s.frame_final_end == selection[0].frame_final_end:
                selection.append(s)
    return selection
