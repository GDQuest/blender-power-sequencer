import bpy
from .utils.global_settings import SequenceTypes


class GrabSequencesHandles(bpy.types.Operator):
    """
    Extends the selected sequences based on the mouse position.
    If the cursor is to the right of the sequence's middle,
    it moves the right handle.
    If it's on the left side, it moves the left handle.
    If effect strips are selected, selects the input strips instead.
    """
    bl_idname = 'power_sequencer.grab_sequence_handle'
    bl_label = 'Grab Sequence Handles'
    bl_description = "Grabs the sequence's handle based on the mouse position"
    bl_options = {'REGISTER', 'UNDO'}

    frame = 0

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        selection = bpy.context.selected_sequences

        if not selection:
            return {'CANCELLED'}

        self.frame, _ = context.region.view2d.region_to_view(
            x=event.mouse_region_x,
            y=event.mouse_region_y)

        bpy.ops.sequencer.select_all(action='DESELECT')
        for s in selection:
            if s.type in SequenceTypes.EFFECT:
                self.select_closest_handle(s.input_1)
                try:
                    self.select_closest_handle(s.input_2)
                except AttributeError:
                    pass
            else:
                self.select_closest_handle(s)

        bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
        return {'FINISHED'}

    def select_closest_handle(self, sequence):
        middle = sequence.frame_final_start + sequence.frame_final_duration / 2
        if self.frame >= middle:
            sequence.select_right_handle = True
        else:
            sequence.select_left_handle = True
        sequence.select = True
