"""Toggle mute a sequence as you click on it"""
import bpy
from math import floor
from .utils.find_strips_mouse import find_strips_mouse


class MouseToggleMute(bpy.types.Operator):
    bl_idname = "power_sequencer.mouse_toggle_mute"
    bl_label = "PS.Mouse toggle mute"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context is not None

    def invoke(self, context, event):
        sequencer = bpy.ops.sequencer

        # get current frame and channel the mouse hovers
        x, y = context.region.view2d.region_to_view(
            x=event.mouse_region_x, y=event.mouse_region_y)
        frame, channel = round(x), floor(y)

        # Strip selection
        sequencer.select_all(action='DESELECT')
        to_select = find_strips_mouse(frame, channel)

        if not to_select:
            return {"CANCELLED"}

        for s in to_select:
            s.mute = not s.mute
        return {"FINISHED"}
