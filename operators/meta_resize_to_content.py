import bpy
from .utils.get_frame_range import get_frame_range

class MetaResizeToContent(bpy.types.Operator):
    """
    Moves the handles of the selected metastrip so it fits its content.
    Use it to trim a metastrip quickly
    """
    bl_idname = "power_sequencer.meta_resize_to_content"
    bl_label = "Meta Resize to Content"
    bl_description = "Moves the handles of the selected metastrip so it fits its content."
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return next(s for s in bpy.context.selected_sequences if s.type == 'META')

    def execute(self, context):
        selected_meta_strips = (s for s in bpy.context.selected_sequences if s.type == 'META')
        for s in selected_meta_strips:
            s.frame_final_start, s.frame_final_end = get_frame_range(s.sequences)
        return {'FINISHED'}
