"""
Trims strips in the timeline between the start and end frame. The caller must pass strips to select
"""
import bpy
from .global_settings import SequenceTypes


def trim_strips(context,
                start_frame, end_frame, select_mode,
                strips_to_trim=[], strips_to_delete=[]):
    """
    Remove the footage and audio between start_frame and end_frame.

    """
    trim_start = min(start_frame, end_frame)
    trim_end = max(start_frame, end_frame)

    strips_to_trim = [s for s in strips_to_trim if s.type in SequenceTypes.CUTABLE]

    for s in strips_to_trim:
        if s.frame_final_start < trim_start and s.frame_final_end > trim_end:
            bpy.ops.sequencer.select_all(action='DESELECT')
            s.select = True
            bpy.ops.sequencer.cut(frame=trim_start, type='SOFT', side='RIGHT')
            bpy.ops.sequencer.cut(frame=trim_end, type='SOFT', side='LEFT')
            strips_to_delete.append(context.selected_sequences[0])
            continue
        elif s.frame_final_start < trim_end and s.frame_final_end > trim_end:
            s.frame_final_start = trim_end
        elif s.frame_final_end > trim_start and s.frame_final_start < trim_start:
            s.frame_final_end = trim_start

    if strips_to_delete != []:
        bpy.ops.sequencer.select_all(action='DESELECT')
        for s in strips_to_delete:
            s.select = True
        bpy.ops.sequencer.delete()
    return {'FINISHED'}

