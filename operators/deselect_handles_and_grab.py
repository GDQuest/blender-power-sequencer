import bpy


class DeselectHandlesAndGrab(bpy.types.Operator):
    """
    Deselect the handles of all selected strips and call the
    Sequence Slide operator
    """
    bl_idname = 'power_sequencer.deselect_handles_and_grab'
    bl_label = 'Deselect Handles And Grab'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for s in bpy.context.selected_sequences:
            s.select_left_handle = False
            s.select_right_handle = False
            s.select = True

        bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
        return {'FINISHED'}
