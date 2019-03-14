import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_trim_left_or_right_handles(bpy.types.Operator):
    """
    Trims, extends and snaps selected strips to cursor
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'K', 'value': 'PRESS', 'alt': True}, {'side': 'right', 'ripple': 'dont_use'}, 'Smart Snap Right'),
            ({'type': 'K', 'value': 'PRESS', 'alt': True, 'shift': True}, {'side': 'right', 'ripple': 'use'}, 'Smart Snap Right With Ripple'),
            ({'type': 'K', 'value': 'PRESS', 'ctrl': True}, {'side': 'left', 'ripple': 'dont_use'}, 'Smart Snap Left'),
            ({'type': 'K', 'value': 'PRESS', 'ctrl': True, 'shift': True}, {'side': 'left', 'ripple': 'use'}, 'Smart Snap Left With Ripple')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    side: bpy.props.EnumProperty(
        items=[('left', 'Left', 'Left side'), ('right', 'Right', 'Right side'),
               ('auto', 'Auto', 'Use the side closest to the time cursor')],
        name="Snap side",
        description="Handle side to use for the snap",
        default='auto')

    ripple: bpy.props.EnumProperty(
        items=[('use', 'Ripple', 'Use ripple'), ('dont_use', "Don't ripple", 'Do not use ripple')],
        name="Use ripple",
        description="Determines if sequences should be rippled",
        default='dont_use')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        frame_current = context.scene.frame_current
        self.select_strip_handle(context.selected_sequences, self.side, frame_current)
        bpy.ops.sequencer.snap(frame=frame_current)

        if self.ripple == 'use':
            for s in context.selected_sequences:
                self.ripple_sequences(s, context)

        for s in context.selected_sequences:
            s.select_right_handle = False
            s.select_left_handle = False
        return {"FINISHED"}

    def select_strip_handle(self, sequences, side, frame):
        """
        Select the left or right handles of the strips based on the frame number
        """
        side = side.upper()
        for s in sequences:
            s.select_left_handle = False
            s.select_right_handle = False

            handle_side = ''
            start, end = s.frame_final_start, s.frame_final_end
            if side == 'AUTO' and start <= frame <= end:
                handle_side = 'LEFT' if abs(
                    frame - start) < s.frame_final_duration / 2 else 'RIGHT'
            elif side == 'LEFT' and frame < end or side == 'RIGHT' and frame > start:
                handle_side = side
            else:
                s.select = False
            if handle_side:
                bpy.ops.sequencer.select_handles(side=handle_side)

    def ripple_sequences(self, sequence, context):
        gap = 0
        side = 'RIGHT' if sequence.select_right_handle else 'LEFT'
        if side == 'RIGHT':
            gap = sequence.frame_final_start + sequence.frame_duration - sequence.frame_final_end
        else:
            gap = abs(sequence.frame_start - sequence.frame_final_start)

        for s in context.sequences:
            if s == sequence or s.channel != sequence.channel:
                continue
            if side == 'RIGHT' and sequence.frame_final_end < s.frame_final_start:
                s.frame_start -= gap
            elif side == 'LEFT' and sequence.frame_final_start > s.frame_final_end:
                s.frame_start += gap
