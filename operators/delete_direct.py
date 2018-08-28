import bpy
from .utils.global_settings import SequenceTypes


class DeleteDirect(bpy.types.Operator):
    """Deletes without prompting for confirmation"""
    bl_idname = "power_sequencer.delete_direct"
    bl_label = "Delete Direct"
    bl_description = "Delete without confirmation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = bpy.context.selected_sequences
        selection_length = len(selection)

        bpy.ops.power_sequencer.crossfade_remove()
        for s in selection:
            try:
                s.select = True
            except:
                pass
        bpy.ops.sequencer.delete()

        report_message = 'Deleted ' + str(selection_length) + ' sequence'
        report_message += 's' if selection_length > 1 else ''
        self.report({'INFO'}, report_message)
        return {"FINISHED"}
