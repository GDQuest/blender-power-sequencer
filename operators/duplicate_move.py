import bpy
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel


class DuplicateMove(bpy.types.Operator):
    """
    Extends Blender's default duplicate tool to add auto-select support.
    """
    bl_idname = 'power_sequencer.duplicate_move'
    bl_label = 'Duplicate Move'
    bl_description = "Auto selects the strip under the mouse if nothing is selected, and calls Blender's Duplicate Move function"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.sequences

    def invoke(self, context, event):
        frame, channel = get_mouse_frame_and_channel(event)
        if not context.selected_sequences:
            bpy.ops.power_sequencer.select_closest_to_mouse(frame=frame, channel=channel)
        return self.execute(context)

    def execute(self, context):
        bpy.ops.sequencer.duplicate_move('INVOKE_DEFAULT')
        return {'FINISHED'}
