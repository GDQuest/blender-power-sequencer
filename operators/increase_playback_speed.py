import bpy
from .utils import update_playback


class IncreasePlaybackSpeed(bpy.types.Operator):
    """
    Playback speed may be set to any of the following speeds:

    * Normal (1x)
    * Fast (1.33x)
    * Faster (1.66x)
    * Double (2x)
    * Triple (3x)

    Activating this operator will increase playback speed through each
    of these steps until maximum speed is reached.
    """
    bl_idname = "power_sequencer.increase_playback_speed"
    bl_label = "Increase Playback Speed"
    bl_description = "Increase playback speed up to triple"

    def execute(self, context):
        scene = context.scene

        speeds = ["normal", "fast", "faster", "double", "triple"]
        current_speed = scene.power_sequencer.playback_speed

        try:
            index = speeds.index(current_speed) + 1
            new_speed = speeds[index]
        except IndexError:
            new_speed = "triple"

        scene.power_sequencer.playback_speed = new_speed

        update_playback()

        return {"FINISHED"}
