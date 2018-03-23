import bpy
from math import floor

from bpy.props import BoolProperty, IntProperty, EnumProperty

from .utils.find_strips_mouse import find_strips_mouse
from .utils.trim_strips import trim_strips
from .utils.get_frame_range import get_frame_range


class MouseTrim(bpy.types.Operator):
    """
    Trims a frame range or a selection from a start to an end frame.
    If there's no precise time range, auto trims based on the closest cut

    Args:
    - frame_start and frame_end (int) define the frame range to trim
    """
    bl_idname = "power_sequencer.mouse_trim"
    bl_label = "Mouse Trim Strips"
    bl_description = "Trim strip from a start to an end frame"
    bl_options = {'REGISTER', 'UNDO'}

    select_mode = EnumProperty(
        items=[('mouse', 'Mouse',
                'Only select the strip hovered by the mouse'),
               ('cursor', 'Time cursor',
                'Select all of the strips the time cursor overlaps'),
               ('smart', 'Smart',
                'Uses the selection if possible, else uses the other modes')],
        name="Selection mode",
        description="Auto-select the strip you click on or that the time cursor overlaps",
        default='smart')
    select_linked = BoolProperty(
        name="Use linked time",
        description="If auto-select, cut linked strips if checked",
        default=False)
    remove_gaps = BoolProperty(
        name="Remove gaps",
        description="When trimming the sequences, remove gaps automatically",
        default=True)

    frame_start, frame_end = IntProperty(), IntProperty()
    to_select = []
    
    function = bpy.props.StringProperty("")

    @classmethod
    def poll(cls, context):
        return context.sequences is not None

    def invoke(self, context, event):
        to_select = []
        if not self.frame_start or self.frame_end:
            x, y = context.region.view2d.region_to_view(
                x=event.mouse_region_x, y=event.mouse_region_y)
            frame, channel = round(x), floor(y)

            mouse_clicked_strip = find_strips_mouse(frame, channel,
                                                    self.select_linked)
            if self.select_mode == 'smart' and mouse_clicked_strip:
                self.select_mode = 'mouse'
            else:
                self.select_mode = 'cursor'

            if self.select_mode == 'mouse':
                if mouse_clicked_strip == []:
                    return {'CANCELLED'}
                to_select.extend(mouse_clicked_strip)
            if self.select_mode == 'cursor':
                for s in bpy.context.sequences:
                    if s.frame_final_start <= frame <= s.frame_final_end:
                        to_select.append(s)

            selection_start, selection_end = get_frame_range(to_select)
            self.frame_start = frame
            self.frame_end = selection_end if abs(frame - selection_end) <= abs(frame - selection_start) else selection_start

        self.to_select = to_select
        trim_strips(self.frame_start, self.frame_end,
                    self.select_mode, self.to_select)

        if self.remove_gaps and self.select_mode == 'cursor':
            bpy.context.scene.frame_current = min(self.frame_start, self.frame_end)
            bpy.ops.sequencer.gap_remove()
        else:
            bpy.context.scene.frame_current = frame
        return {'FINISHED'}
