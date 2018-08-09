import bpy
from math import floor

from .utils.find_strips_mouse import find_strips_mouse
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
        return True

    def invoke(self, context, event):
        frame, channel = get_mouse_frame_and_channel(event)

        sequences = find_strips_mouse(frame, channel, select_linked=True)
        if not sequences:
            return {'CANCELLED'}

        user_selection = bpy.context.selected_sequences
        bpy.ops.sequencer.select_all(action='DESELECT')
        for s in sequences:
            s.select = True
        bpy.ops.power_sequencer.smart_snap(side=self.side)
        # FIXME: remove the need for that crap
        for s in user_selection:
            s.select = True
        return {'FINISHED'}
