import bpy

def convert_duration_to_frames(duration):
    return round(duration * bpy.context.scene.render.fps / bpy.context.scene.render.fps_base)
