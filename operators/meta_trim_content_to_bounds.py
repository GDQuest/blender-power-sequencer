import bpy
from .utils.global_settings import SequenceTypes


class MetaTrimContentToBounds(bpy.types.Operator):
    bl_idname = "power_sequencer.meta_trim_content_to_bounds"
    bl_label = "Meta Trim Content to Bounds"
    bl_description = "Deletes and trims the strips inside selected meta-strips to the meta strip's bounds"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            next(s for s in context.selected_sequences if s.type == 'META')
            return True
        except StopIteration:
            return False

    def execute(self, context):
        to_delete = []
        meta_strips = [s for s in context.selected_sequences if s.type == 'META']
        for m in meta_strips:
            start, end = m.frame_final_start, m.frame_final_end
            sequences_to_process = (s for s in m.sequences if s.type not in SequenceTypes.EFFECT)
            for s in sequences_to_process:
                if s.frame_final_end < start or s.frame_final_start > m.frame_final_end:
                    to_delete.append(s)
                    continue
                # trim strips on the meta's edges or longer than the meta's extents
                if s.frame_final_start < start:
                    s.frame_final_start = start
                if s.frame_final_end > end:
                    s.frame_final_end = end
        bpy.ops.sequencer.select_all(action='DESELECT')
        for s in to_delete:
            s.select = True
        bpy.ops.sequencer.delete()
        return {'FINISHED'}
