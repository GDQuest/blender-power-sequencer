import bpy

from bpy.props import BoolProperty
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description

class MergeFromSceneStrip(bpy.types.Operator):
    """
    *brief* Copies all sequences and markers from a SceneStrip's scene into
    the active scene. Optionally delete the source scene and the strip.


    WARNING: Currently the operator doesn't recreate any animation data,
    be careful by choosing to delete the scene after the merge.
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

    delete_scene = BoolProperty(
            name = "Delete Strip's scene",
            description = "Delete the SceneStrip's scene after the merging",
            default = True
    )

    @classmethod
    def poll(cls, context):
        return context.scene.sequence_editor.active_strip.type == 'SCENE'

    def invoke(self, context, event):
        window_manager = context.window_manager
        return window_manager.invoke_props_dialog(self)

    def execute(self, context):
        strip = context.scene.sequence_editor.active_strip
        strip_scene = strip.scene
        start_scene = context.screen.scene

        self.merge_markers(strip_scene, start_scene)
        self.merge_strips(strip_scene, start_scene)

        if not self.delete_scene:
            return {'FINISHED'}

        bpy.ops.sequencer.select_all(action = 'DESELECT')
        strip.select = True
        bpy.ops.sequencer.delete()
        context.screen.scene = strip_scene
        bpy.ops.scene.delete()
        context.screen.scene = start_scene
        self.report(type = {'WARNING'}, message = "All animations on source scene were lost")

        return {'FINISHED'}

    def merge_strips(self, source_scene, target_scene):
        bpy.context.screen.scene = source_scene
        bpy.ops.sequencer.select_all(action = 'SELECT')
        bpy.ops.sequencer.copy()

        bpy.context.screen.scene = target_scene
        current_frame = bpy.context.scene.frame_current
        active = bpy.context.scene.sequence_editor.active_strip
        bpy.context.scene.frame_current = active.frame_final_start
        bpy.ops.sequencer.select_all(action = 'DESELECT')
        bpy.ops.sequencer.paste()

        bpy.context.scene.frame_current = current_frame


    def merge_markers(self, source_scene, target_scene):
        if len(target_scene.timeline_markers) > 0:
            bpy.ops.marker.select_all(action = 'DESELECT')

        bpy.context.screen.scene = source_scene
        bpy.ops.marker.select_all(action = 'SELECT')
        bpy.ops.marker.make_links_scene(scene = target_scene.name)

        bpy.context.screen.scene = target_scene
        active = bpy.context.screen.scene.sequence_editor.active_strip
        time_offset = active.frame_final_start
        bpy.ops.marker.move(frames = time_offset)
        bpy.ops.marker.select_all(action = 'DESELECT')
