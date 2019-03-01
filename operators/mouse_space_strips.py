import bpy
import operator

from .utils.get_mouse_view_coords import get_mouse_frame_and_channel
from .utils.convert_duration_to_frames import convert_duration_to_frames
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_mouse_space_strips(bpy.types.Operator):
    """
    *brief* Offsets all strips to the right of the mouse cursor by a given duration


    Default shortcut: <kbd>=</kbd>
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'EQUAL', 'value': 'PRESS'}, {}, '')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    gap_to_insert: bpy.props.FloatProperty(
        name="Duration",
        description="The time offset to apply to the strips",
        default=1.0)

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0

    def invoke(self, context, event):
        gap_frames = convert_duration_to_frames(context, self.gap_to_insert)
        strips_to_space = []
        frame, _ = get_mouse_frame_and_channel(context, event)

        for s in context.sequences:
            if s.frame_final_start >= frame:
                strips_to_space.append(s)

        sorted_strips = sorted(strips_to_space, key=operator.attrgetter('frame_start'), reverse=True)

        for s in sorted_strips:
            s.frame_start += gap_frames
        return {'FINISHED'}
