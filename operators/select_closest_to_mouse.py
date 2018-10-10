import bpy
from .utils.find_strips_mouse import find_strips_mouse
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel

class SelectClosestToMouse(bpy.types.Operator):
    bl_idname = 'power_sequencer.select_closest_to_mouse'
    bl_label = 'Select Closest to Mouse'
    bl_description = 'Select the closest strip under the mouse cursor'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        mouse = get_mouse_frame_and_channel(event)
        strip = find_strips_mouse(mouse[0], mouse[1])[0]
        strip.select = True
        return {"FINISHED"}
