import bpy
from .utils.find_closest_strip import find_closest_strip


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
        if len(bpy.context.selected_sequences) == 0:
            closest_strip = find_closest_strip(bpy.context.sequences, event.mouse_x, event.mouse_y)
            closest_strip.select = True
        return self.execute(context)

    def execute(self, context):
        return bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
