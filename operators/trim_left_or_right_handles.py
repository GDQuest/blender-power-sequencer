from operator import attrgetter

import bpy

from .utils.doc import doc_brief, doc_description, doc_idname, doc_name


class POWER_SEQUENCER_OT_trim_left_or_right_handles(bpy.types.Operator):
    """
    Trims or extends the handle closest to the time cursor for all selected strips.

    If you keep the Shift key down, the edit will ripple through the timeline.
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'K', 'value': 'PRESS', 'alt': True}, {'side': 'RIGHT', 'ripple': False, 'auto_select': False}, 'Smart Snap Right'),
            ({'type': 'K', 'value': 'PRESS', 'alt': True, 'shift': True}, {'side': 'RIGHT', 'ripple': True, 'auto_select': False}, 'Smart Snap Right With Ripple'),
            ({'type': 'K', 'value': 'PRESS', 'ctrl': True}, {'side': 'LEFT', 'ripple': False, 'auto_select': False}, 'Smart Snap Left'),
            ({'type': 'K', 'value': 'PRESS', 'ctrl': True, 'shift': True}, {'side': 'LEFT', 'ripple': True, 'auto_select': False}, 'Smart Snap Left With Ripple'),
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    side: bpy.props.EnumProperty(
        items=[('LEFT', 'Left', 'Left side'),
               ('RIGHT', 'Right', 'Right side'),],
        name="Snap side",
        description="Handle side to use for the snap",
        default='LEFT')
    ripple: bpy.props.BoolProperty(
        name="Ripple",
        default=False)

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0

    def execute(self, context):
        frame_current = context.scene.frame_current

        sequences = context.selected_sequences if context.selected_sequences else context.sequences
        for s in sequences:
            s.select = s.frame_final_start <= frame_current and s.frame_final_end >= frame_current
        sequences = [s for s in sequences if s.select]
        for s in sequences:
            if self.side == 'LEFT':
                s.select_left_handle = True
            if self.side == 'RIGHT':
                s.select_right_handle = True

        bpy.ops.sequencer.snap(frame=frame_current)

        for s in sequences:
            s.select_right_handle = False
            s.select_left_handle = False

        # FIXME: quick hack
        # Should use a function instead of the operator
        if self.ripple:
            bpy.ops.sequencer.gap_remove()
        return {"FINISHED"}
