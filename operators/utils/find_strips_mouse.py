def find_strips_mouse(context, frame, channel, select_linked=False):
    """
    Finds a list of sequences to select based on the mouse position
    or using the time cursor.

    Args:
    - frame: the frame the mouse or cursor is on
    - channel: the channel the mouse is hovering
    - select_linked: find and append the sequences linked in time if True

    Returns the sequence(s) under the mouse cursor as a list
    Returns an empty list if nothing found
    """
    sequences = [s for s in context.sequences if not s.lock and s.channel == channel]
    try:
        under_mouse = [
            next(s for s in sequences if s.frame_final_start <= frame <= s.frame_final_end)
        ]
    except StopIteration:
        return []

    if select_linked:
        linked_strips = [
            s
            for s in sequences
            if s.frame_final_start == under_mouse[0].frame_final_start
            and s.frame_final_end == under_mouse[0].frame_final_end
        ]
        return under_mouse.append(linked_strips)
    else:
        return under_mouse
