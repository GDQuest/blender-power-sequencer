import bpy
import operator

from bpy.props import StringProperty
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description

class RenameStripScene(bpy.types.Operator):
    """
    Rename a Scene Strip and its source scene.
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [],
        'keymap': 'Sequencer'
    }
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
    bl_options = {"REGISTER", "UNDO"}

    new_name = StringProperty(
        name="Strip New Name",
        description="The name both the SceneStrip and its source Scene will take",
        default="")

    @classmethod
    def poll(cls, context):
        return context.scene.sequence_editor.active_strip.type == 'SCENE'

    def invoke(self, context, event):
        window_manager = context.window_manager
        return window_manager.invoke_props_dialog(self)

    def execute(self, context):
        strip = context.scene.sequence_editor.active_strip
        strip_scene = strip.scene

        strip.name = self.new_name
        strip_scene.name = strip.name
        return {'FINISHED'}
