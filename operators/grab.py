import bpy
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel
from .utils.global_settings import SequenceTypes


class Grab(bpy.types.Operator):
    """
    This feature builds upon and extends Blender's default Grab tool
    It auto selects the strip closest to the mouse cursor if you don't have anything selected
    """
    bl_idname = "power_sequencer.grab"
    bl_label = "Grab sequences"
    bl_description = "Grab and move sequences. Extends Blender's built-in grab tool"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context is not None

    def invoke(self, context, event):
        frame, channel = get_mouse_frame_and_channel(event)
        if not context.selected_sequences:
            bpy.ops.power_sequencer.select_closest_to_mouse(frame=frame, channel=channel)
        return self.execute(context)

    def execute(self, context):
        first_sequence = bpy.context.selected_sequences[0]
        if len(bpy.context.selected_sequences) == 1 and first_sequence.type in SequenceTypes.TRANSITION:
            bpy.context.scene.sequence_editor.active_strip = first_sequence
            return bpy.ops.power_sequencer.crossfade_edit()
        return bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
