import bpy
from operator import attrgetter


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
