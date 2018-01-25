import bpy


class ChangePlaybackSpeed(bpy.types.Operator):
    """
    Change the playback_speed property using an operator property.
    Used with keymaps
    """
    bl_idname = "power_sequencer.change_playback_speed"
    bl_label = "Change Playback Speed"
    bl_description = "Change the playback speed"

    bl_options = {"REGISTER"}

    speed = bpy.props.EnumProperty(
        items=[('normal', 'Normal (1x)', ''), ('fast', 'Fast (1.33x)', ''),
               ('faster', 'Faster (1.66x)', ''), ('double', 'Double (2x)', ''),
               ('triple', 'Triple (3x)', '')],
        name='Speed',
        description='Change the playback speed',
        default='double')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.scene.power_sequencer.playback_speed = self.speed
        return {"FINISHED"}