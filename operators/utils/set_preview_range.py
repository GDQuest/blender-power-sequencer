import bpy


def set_preview_range(start, end):
    """Sets the preview range and timeline render range"""
    if not (start and end) and start != 0:
        raise AttributeError('Missing start or end parameter')

    scene = bpy.context.scene

    scene.frame_start = start
    scene.frame_end = end
    scene.frame_preview_start = start
    scene.frame_preview_end = end