def convert_duration_to_frames(context, duration):
    return round(duration * context.scene.render.fps / context.scene.render.fps_base)
