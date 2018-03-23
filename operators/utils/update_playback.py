import bpy


def update_playback():
    """
    This is to update the playback speed when it is changed when not
    playing.

    Apparently redrawing Blender like this is bad, even if it works::

        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    See:
    https://docs.blender.org/api/blender_python_api_2_78_release/info_gotcha.html

    Instead, we can trigger an update by jostling it's current frame.
    """

    scene = bpy.context.scene
    scrubbing = False

    if scene.use_audio_scrub:
        scrubbing = True
        scene.use_audio_scrub = False

    scene.frame_current += 1
    scene.frame_current -= 1

    if scrubbing:
        scene.use_audio_scrub = True

