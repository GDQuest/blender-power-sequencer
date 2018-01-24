import bpy


class GrabSequenceHandle(bpy.types.Operator):
    """
    Extends the sequence based on the mouse position.
    If the cursor is to the right of the sequence's middle,
    it moves the right handle.
    If it's on the left side, it moves the left handle.
    """
    bl_idname = 'power_sequencer.grab_sequence_handle'
    bl_label = 'Grab sequence handles'
    bl_description = 'Grabs the sequence\'s handle based on the mouse position'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        selection = bpy.context.selected_sequences
        if not selection:
            return {'CANCELLED'}

        frame, _ = context.region.view2d.region_to_view(
            x=event.mouse_region_x, y=event.mouse_region_y)

        bpy.ops.sequencer.select_all(action='DESELECT')
        for s in selection:
            middle = s.frame_final_start + s.frame_final_duration / 2
            if frame >= middle:
                s.select_right_handle = True
            else:
                s.select_left_handle = True
            s.select = True

        bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
        return {'FINISHED'}
