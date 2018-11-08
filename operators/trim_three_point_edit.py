import bpy
from math import floor

from .utils.get_mouse_view_coords import get_mouse_frame_and_channel


class TrimThreePointEdit(bpy.types.Operator):
    bl_idname = 'power_sequencer.trim_three_point_edit'
    bl_label = 'Three Point edit'
    bl_description = "Trim the closest strip under the mouse cursor in or out"
    bl_options = {'REGISTER', 'UNDO'}

    side = bpy.props.EnumProperty(
        items=[
            ('left', 'Left', 'Left side'),
            ('right', 'Right', 'Right side'),
        ],
        name="Trim side",
        description="Side of the strip(s) to trim, either left or right",
        default='left')

    @classmethod
    def poll(cls, context):
        return context.sequences

    def invoke(self, context, event):
        frame, channel = get_mouse_frame_and_channel(event)
        bpy.ops.sequencer.select_all(action='DESELECT')
        bpy.ops.power_sequencer.select_closest_to_mouse(
            frame=frame, channel=channel)
        if not bpy.context.selected_sequences:
            bpy.ops.power_sequencer.select_strips_under_cursor()
        return self.execute(context)

    def execute(self, context):
        if not bpy.context.selected_sequences:
            return {'CANCELLED'}
        bpy.ops.power_sequencer.smart_snap(side=self.side)
        return {'FINISHED'}
