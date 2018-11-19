import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description

class OpenSceneStrip(bpy.types.Operator):
    """
    Sets the current scene to the scene in the SceneStrip
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
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.scene.sequence_editor.active_strip.type == 'SCENE'

    def execute(self, context):
        strip_scene = context.scene.sequence_editor.active_strip.scene
        context.screen.scene = bpy.data.scenes[strip_scene.name]

        return {'FINISHED'}
