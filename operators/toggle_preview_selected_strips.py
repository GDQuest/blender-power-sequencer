import bpy
from .utils.get_frame_range import get_frame_range
from .utils.set_preview_range import set_preview_range


class TogglePreviewSelectedStrips(bpy.types.Operator):
    """Sets the preview range based on selected sequences"""
    bl_idname = "power_sequencer.toggle_preview_selected_strips"
    bl_label = "Toggle Preview Selected Strips"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = bpy.context.scene
        selection = bpy.context.selected_sequences
        if not selection:
            return {'CANCELLED'}
        frame_start, frame_end = get_frame_range(
            sequences=bpy.context.selected_sequences, get_from_start=False)

        if scene.frame_start == frame_start and scene.frame_end == frame_end:
            frame_start, frame_end = get_frame_range(get_from_start=True)

        set_preview_range(frame_start, frame_end)
        return {'FINISHED'}
