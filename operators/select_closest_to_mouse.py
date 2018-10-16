import bpy
from .utils.find_strips_mouse import find_strips_mouse
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel

class SelectClosestToMouse(bpy.types.Operator):
    bl_idname = 'power_sequencer.select_closest_to_mouse'
    bl_label = 'Select Closest to Mouse'
    bl_description = 'Select the closest strip under the mouse cursor'
    bl_options = {'REGISTER', 'UNDO'}

    frame = bpy.props.IntProperty(name="Frame")
    channel = bpy.props.IntProperty(name="Channel")

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        self.frame, self.channel = get_mouse_frame_and_channel(event)
        return self.execute(context)

    def execute(self, context):
        try:
            strip = find_strips_mouse(self.frame, self.channel)[0]
            strip.select = True
        except Exception:
            return {"CANCELLED"}
        return {"FINISHED"}
