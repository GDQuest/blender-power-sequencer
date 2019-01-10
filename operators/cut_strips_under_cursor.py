import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel


class CutStripsUnderCursor(bpy.types.Operator):
    """
    Cuts all strips under cursor (without needing selection first), including mutted strips. It
    excludes locked strips.
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'K', 'value': 'PRESS'}, {}, 'Cut All Strips Under Cursor')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    side = bpy.props.EnumProperty(
        items=[('LEFT', '', ''),
               ('RIGHT', '', '')],
        name='Side',
        default='LEFT',
        options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0

    def invoke(self, context, event):
        frame, channel = get_mouse_frame_and_channel(context, event)
        self.side = 'LEFT' if frame < context.scene.frame_current else 'RIGHT'
        return self.execute(context)

    def execute(self, context):
        # Deselect to trigger a call to select_strips_under_cursor below if the
        # time cursor doesn't overlap any of the selected strip: if so, it
        # can't cut anything!
        deselect = True
        for s in bpy.context.selected_sequences:
            if s.frame_final_start <= context.scene.frame_current <= s.frame_final_end:
                deselect = False
        if deselect:
            bpy.ops.sequencer.select_all(action='DESELECT')
        (context.selected_sequences
         or bpy.ops.power_sequencer.select_strips_under_cursor())
        return bpy.ops.sequencer.cut(frame=context.scene.frame_current, side=self.side)
