import bpy


def find_neighboring_markers(frame=None):
    """Returns a tuple containing the closest marker to the left and to the right of the frame"""
    markers = bpy.context.scene.timeline_markers

    if not (frame and markers):
        return None, None

    from operator import attrgetter
    markers = sorted(markers, key=attrgetter('frame'))

    previous_marker, next_marker = None, None
    for m in markers:
        previous_marker = m if m.frame < frame else previous_marker
        if m.frame > frame:
            next_marker = m
            break

    return previous_marker, next_marker
