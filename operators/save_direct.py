import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class SaveDirect(bpy.types.Operator):
    """
    Saves current file without prompting for confirmation. Overrides Blender deafult
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'S', 'value': 'PRESS', 'ctrl': True}, {}, 'Direct Save')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if bpy.data.is_saved:
            bpy.ops.wm.save_mainfile()
        else:
            bpy.ops.wm.save_as_mainfile({'dict': "override"}, 'INVOKE_DEFAULT')
        self.report({'INFO'}, 'File saved')
        return {"FINISHED"}

