import bpy
import os
from platform import system
from subprocess import Popen

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class OpenProjectDirectory(bpy.types.Operator):
    """
    Opens the Blender project directory in file explorer
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
        path = os.path.split(bpy.data.filepath)[0]

        if not path:
            self.report({'INFO'}, "You have to save your project first.")
            return {'CANCELLED'}

        if system() == "Windows":
            Popen(["explorer", path])
        elif system() == "Darwin":
            Popen(["open", path])
        else:
            Popen(["xdg-open", path])
        return {'FINISHED'}

