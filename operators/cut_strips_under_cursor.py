import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class CutStripsUnderCursor(bpy.types.Operator):
    """
    Cuts all strips under cursor (without needing selection first), including mutted strips. It
    excludes locked strips.
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': 'https://i.imgur.com/ZyEd0jD.gif',
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

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0

    def execute(self, context):
        (context.selected_sequences
         or bpy.ops.power_sequencer.select_strips_under_cursor())
        return bpy.ops.sequencer.cut(frame=context.scene.frame_current)

