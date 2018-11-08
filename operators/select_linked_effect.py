import bpy

from .utils.find_linked_sequences import find_linked
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class SelectLinkedEffect(bpy.types.Operator):
    """
    Select all strips that are linked by an effect strip
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
        return True

    def execute(self, context):
        for s in find_linked(bpy.context.selected_sequences):
            s.select = True
        return {'FINISHED'}

