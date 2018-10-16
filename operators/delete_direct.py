import bpy
from .utils.global_settings import SequenceTypes
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel


class DeleteDirect(bpy.types.Operator):
    """Deletes without prompting for confirmation"""
    bl_idname = "power_sequencer.delete_direct"
    bl_label = "Delete Direct"
    bl_description = "Delete without confirmation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0

    def invoke(self, context, event):
        frame, channel = get_mouse_frame_and_channel(event)
        if not context.selected_sequences:
            bpy.ops.power_sequencer.select_closest_to_mouse(frame=frame, channel=channel)
        return self.execute(context)

    def execute(self, context):
        selection = bpy.context.selected_sequences
        if bpy.ops.power_sequencer.crossfade_remove.poll():
            bpy.ops.power_sequencer.crossfade_remove()
        bpy.ops.sequencer.delete()

        report_message = 'Deleted ' + str(len(selection)) + ' sequence'
        report_message += 's' if len(selection) > 1 else ''
        self.report({'INFO'}, report_message)
        return {"FINISHED"}
