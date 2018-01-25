import bpy


class DecreasePlaybackSpeed(bpy.types.Operator):
    """
    Playback speed may be set to any of the following speeds:

    * Normal (1x)
    * Fast (1.33x)
    * Faster (1.66x)
    * Double (2x)
    * Triple (3x)

    Activating this operator will decrease playback speed through each
    of these steps until minimum speed is reached.
    """
    bl_idname = "power_sequencer.decrease_playback_speed"
    bl_label = "Decrease Playback Speed"
    bl_description = "Decrease playback speed down to normal"

    def execute(self, context):
        scene = context.scene

        speeds = ["normal", "fast", "faster", "double", "triple"]
        current_speed = scene.power_sequencer.playback_speed

        index = speeds.index(current_speed) - 1
        if index < 0:
            index = 0
        new_speed = speeds[index]

        scene.power_sequencer.playback_speed = new_speed

        return {"FINISHED"}