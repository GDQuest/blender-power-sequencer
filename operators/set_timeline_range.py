import bpy


class SetTimelineRange(bpy.types.Operator):
    """
    Set the timeline start and end frame using the time cursor
    """
    bl_idname = "power_sequencer.set_timeline_range"
    bl_label = "Set timeline range"
    bl_options = {'REGISTER', 'UNDO'}

    adjust = bpy.props.EnumProperty(
        items=[('start', 'start', 'start'), ('end', 'end', 'end')],
        name='Adjust',
        description='Change the start or the end frame of the timeline',
        default='start')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = bpy.context.scene
        if self.adjust == 'start':
            scene.frame_start = scene.frame_current
        elif self.adjust == 'end':
            scene.frame_end = scene.frame_current - 1
        return {'FINISHED'}
