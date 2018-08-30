import bpy
from operator import attrgetter


def get_frame_range(sequences):
    """
    Returns a tuple with the minimum and maximum frames of the
    list of passed sequences.
    If no sequences are passed, returns the timeline's start and end frames
    Args:
        - sequences, a list of the sequences to use
    """
    if not sequences:
        scene = bpy.context.scene
        return scene.frame_start, scene.frame_end
    start = min(sequences, key=attrgetter('frame_final_start')).frame_final_start
    end = max(sequences, key=attrgetter('frame_final_end')).frame_final_end
    return start, end
