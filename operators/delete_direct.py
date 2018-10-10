import bpy
from .utils.global_settings import SequenceTypes
from .utils.find_strips_mouse import find_strips_mouse
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel


class DeleteDirect(bpy.types.Operator):
    """Deletes without prompting for confirmation"""
    bl_idname = "power_sequencer.delete_direct"
    bl_label = "Delete Direct"
    bl_description = "Delete without confirmation"
    bl_options = {'REGISTER', 'UNDO'}

    frame, channel = None, None

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0

    def invoke(self, context, event):
        self.frame, self.channel = get_mouse_frame_and_channel(event)
        return self.execute(context)

    def execute(self, context):
        start_selection = self.get_start_selection()
        selection_length = len(start_selection)

        if bpy.ops.power_sequencer.crossfade_remove.poll():
            bpy.ops.power_sequencer.crossfade_remove()
        for s in start_selection:
            try:
                s.select = True
            except:
                pass
        bpy.ops.sequencer.delete()

        report_message = 'Deleted ' + str(selection_length) + ' sequence'
        report_message += 's' if selection_length > 1 else ''
        self.report({'INFO'}, report_message)
        return {"FINISHED"}

    def get_start_selection(self):
        """
        Returns a list of strips to use with the delete operator
        If there's no selected_sequences, finds linked strips under the mouse cursor
        """
        strips = bpy.context.selected_sequences
        if strips == []:
            if self.frame is None:
                return []
            strips = find_strips_mouse(self.frame, self.channel, select_linked=True)
            for s in strips:
                s.select = True
        return strips
