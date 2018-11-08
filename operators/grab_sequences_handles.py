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
    bl_idname = 'power_sequencer.grab_sequence_handles'
    bl_label = 'Grab Sequence Handles'
    bl_description = "Grabs the sequence's handle based on the mouse position"
    bl_options = {'REGISTER', 'UNDO'}

    always_find_closest = bpy.props.BoolProperty(name="Always find closest", default=False)
    frame = bpy.props.IntProperty(name="Frame", default=-1, options={'HIDDEN'})
    channel = bpy.props.IntProperty(name="Channel", default=-1, options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0

    def invoke(self, context, event):
        self.frame, self.channel = context.region.view2d.region_to_view(
            x=event.mouse_region_x,
            y=event.mouse_region_y)
        return self.execute(context)

    def execute(self, context):
        selection = bpy.context.selected_sequences
        if self.always_find_closest or not selection:
            if self.frame == -1:
                return {'CANCELLED'}
            bpy.ops.power_sequencer.select_closest_to_mouse(frame=self.frame, channel=self.channel)
            for s in bpy.context.selected_sequences:
                self.select_closest_handle(s)
        else:
            bpy.ops.sequencer.select_all(action='DESELECT')
            for s in selection:
                if s.type in SequenceTypes.EFFECT and not s.type == 'COLOR':
                    self.select_closest_handle(s.input_1)
                    try:
                        self.select_closest_handle(s.input_2)
                    except AttributeError:
                        pass
                else:
                    self.select_closest_handle(s)
        return bpy.ops.transform.seq_slide('INVOKE_DEFAULT')

    def select_closest_handle(self, sequence):
        middle = sequence.frame_final_start + sequence.frame_final_duration / 2
        if self.frame >= middle:
            sequence.select_right_handle = True
        else:
            sequence.select_left_handle = True
        sequence.select = True
