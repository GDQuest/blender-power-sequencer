import bpy


class CycleScenes(bpy.types.Operator):
    """Cycle through scenes"""
    bl_idname = "power_sequencer.cycle_scenes"
    bl_label = "Cycle scenes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

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
