import bpy
from math import floor

from .utils.find_strips_mouse import find_strips_mouse
from .utils.trim_strips import trim_strips
from .utils.get_frame_range import get_frame_range
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_mouse_trim(bpy.types.Operator):
    """
    *brief* Trim strip from a start to an end frame


    Trims a frame range or a selection from a start to an end frame.
    If there's no precise time range, auto trims based on the closest cut

    Args:
    - frame_start and frame_end (int) define the frame range to trim
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'RIGHTMOUSE', 'value': 'PRESS', 'ctrl': True, 'alt': True},
             {'select_mode': 'smart'},
             'Trim strip, keep gap'),
            ({'type': 'RIGHTMOUSE', 'value': 'PRESS', 'ctrl': True, 'alt': True, 'shift': True},
             {'select_mode': 'cursor'},
             'Trim strip, remove gap')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    select_mode: bpy.props.EnumProperty(
        items=[('mouse', 'Mouse',
                'Only select the strip hovered by the mouse'),
               ('cursor', 'Time cursor',
                'Select all of the strips the time cursor overlaps'),
               ('smart', 'Smart',
                'Uses the selection if possible, else uses the other modes')],
        name="Selection mode",
        description="Auto-select the strip you click on or that the time cursor overlaps",
        default='smart')
    select_linked: bpy.props.BoolProperty(
        name="Use linked time",
        description="If auto-select, cut linked strips if checked",
        default=False)
    gap_remove: bpy.props.BoolProperty(
        name="Remove gaps",
        description="When trimming the sequences, remove gaps automatically",
        default=True)

    frame_start: bpy.props.IntProperty()
    frame_end: bpy.props.IntProperty()
    to_select = []

    @classmethod
    def poll(cls, context):
        return context.sequences is not None

    def invoke(self, context, event):
        to_select = []
        frame, channel = 1, 1
        if not self.frame_start or self.frame_end:
            x, y = context.region.view2d.region_to_view(
                x=event.mouse_region_x, y=event.mouse_region_y)
            frame, channel = round(x), floor(y)

            mouse_clicked_strip = find_strips_mouse(context, frame, channel, self.select_linked)
            if self.select_mode == 'smart' and mouse_clicked_strip:
                self.select_mode = 'mouse'
            else:
                self.select_mode = 'cursor'

            if self.select_mode == 'mouse':
                if mouse_clicked_strip == []:
                    return {'CANCELLED'}
                to_select.extend(mouse_clicked_strip)
            if self.select_mode == 'cursor':
                for s in context.sequences:
                    if s.frame_final_start <= frame <= s.frame_final_end:
                        to_select.append(s)

            selection_start, selection_end = get_frame_range(context, to_select)
            self.frame_start = frame
            self.frame_end = (selection_end
                              if abs(frame - selection_end) <= abs(frame - selection_start) else
                              selection_start)

        self.to_select = [s for s in to_select if not s.lock]
        trim_strips(context,
                    self.frame_start, self.frame_end,
                    self.select_mode, self.to_select)

        if self.gap_remove and self.select_mode == 'cursor':
            context.scene.frame_current = min(self.frame_start, self.frame_end)
            bpy.ops.power_sequencer.gap_remove()
        else:
            context.scene.frame_current = self.frame_start if self.frame_start else frame
        return {'FINISHED'}

