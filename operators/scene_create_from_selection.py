import bpy
from operator import attrgetter

class SceneCreateFromSelection(bpy.types.Operator):
    """
    """
    bl_idname = 'power_sequencer.scene_create_from_selection'
    bl_label = 'Scene Create From Selection'
    bl_description = "Create a scene from the selected sequences, copying the current scene's settings, and replace the selection with the newly created scene as a strip"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_sequences) > 0

    def execute(self, context):
        start_scene_name = context.scene.name

        selection = bpy.context.selected_sequences
        selection_start_frame = min(selection, key=attrgetter('frame_final_start')).frame_final_start
        selection_start_channel = min(selection, key=attrgetter('channel')).channel

        # Create new scene for the scene strip
        bpy.ops.scene.new(type='FULL_COPY')
        new_scene_name = bpy.context.scene.name
        bpy.ops.power_sequencer.preview_to_selection()

        bpy.ops.sequencer.select_all(action='INVERT')
        bpy.ops.power_sequencer.delete_direct()

        # Back to start scene
        bpy.context.screen.scene = bpy.data.scenes[start_scene_name]

        bpy.ops.power_sequencer.delete_direct()
        bpy.ops.sequencer.scene_strip_add(frame_start=selection_start_frame, channel=selection_start_channel, scene=new_scene_name)
        scene_strip = bpy.context.selected_sequences[0]
        scene_strip.use_sequence = True
        return {'FINISHED'}
