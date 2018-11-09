import bpy
from .utils.get_frame_range import get_frame_range

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class MetaResizeToContent(bpy.types.Operator):
    """
    *brief* Moves the handles of the selected metastrip so it fits its content.


    Use it to trim a metastrip quickly
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            meta = next(s for s in bpy.context.selected_sequences if s.type == 'META')
        except StopIteration:
            return False
        return True

    def execute(self, context):
        selected_meta_strips = (s for s in bpy.context.selected_sequences if s.type == 'META')
        for s in selected_meta_strips:
            s.frame_final_start, s.frame_final_end = get_frame_range(s.sequences)
        return {'FINISHED'}

