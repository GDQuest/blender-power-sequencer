import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class SceneCycle(bpy.types.Operator):
    """
    Cycle through scenes
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': 'https://i.imgur.com/7zhq8Tg.gif',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'TAB', 'value': 'PRESS', 'shift': True}, {}, 'Cycle Scenes')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(bpy.data.scenes) > 1

    def execute(self, context):
        scenes = bpy.data.scenes

        scene_count = len(scenes)

        if bpy.context.screen.is_animation_playing:
            bpy.ops.screen.animation_cancel(restore_frame=False)
        for index in range(scene_count):
            if bpy.context.scene == scenes[index]:
                bpy.context.screen.scene = scenes[(index + 1) % scene_count]
                break
        return {'FINISHED'}

