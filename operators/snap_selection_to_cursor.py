import bpy
from operator import attrgetter

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class SnapSelectionToCursor(bpy.types.Operator):
    """
    Snap selected strips to the cursor as a block
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'S', 'value': 'PRESS', 'alt': True}, {}, 'Snap selection to cursor')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.selected_sequences and len(context.selected_sequences) > 0)

    def execute(self, context):
        selection = sorted(
            bpy.context.selected_sequences,
            key=attrgetter('frame_final_start'))
        time_move = selection[0].frame_final_start - bpy.context.scene.frame_current

        bpy.ops.power_sequencer.select_related_strips()
        bpy.ops.transform.seq_slide(value=(-time_move, 0))

        return {'FINISHED'}

