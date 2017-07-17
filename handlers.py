"""
All the functions and classes that are related to Blender's handlers.
In other words, everything that runs in the background.
"""
import bpy
from bpy.app.handlers import persistent

# TODO: register in menu
@persistent
def playback_speed(scene):
    scene = bpy.context.scene
    playback_speed = scene.power_sequencer.playback_speed
    if (playback_speed == "fast"):
        if scene.frame_current % 3 == 0:
            scene.frame_current += 1
    elif (playback_speed == "very fast"):
        if scene.frame_current % 2 == 0:
            scene.frame_current += 1