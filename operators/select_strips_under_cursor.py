import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class SelectStripsUnderCursor(bpy.types.Operator):
    """
    Selects the strips that are currently under the time cursor
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': []
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0

    def execute(self, context):
        current_frame = context.scene.frame_current
        sequences_to_select = []
        for s in context.sequences:
            if s.frame_final_start <= current_frame and s.frame_final_end >= current_frame:
                sequences_to_select.append(s)
        if not sequences_to_select:
            return {'CANCELLED'}
        for s in sequences_to_select:
            s.select = True
        return {'FINISHED'}

