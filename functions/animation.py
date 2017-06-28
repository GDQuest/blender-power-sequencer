"""Functions related to animation data like fades, transform, masks., etc."""
import bpy
from .global_settings import SequenceTypes


def add_transform_effect(sequences=None):
    """Takes a list of image strips and adds a transform effect to them.
       Ensures that the pivot will be centered on the image"""
    sequencer = bpy.ops.sequencer
    sequence_editor = bpy.context.scene.sequence_editor
    render = bpy.context.scene.render

    sequences = [s for s in sequences if s.type in ('IMAGE', 'MOVIE')]
    if not sequences:
        return None
    sequencer.select_all(action='DESELECT')

    for s in sequences:
        s.mute = True

        center_img(s)

        sequence_editor.active_strip = s
        sequencer.effect_strip_add(type='TRANSFORM')

        active = sequence_editor.active_strip
        active.name = "TRANSFORM-%s" % s.name
        active.blend_type = 'ALPHA_OVER'
        active.select = False

    print("Successfully processed " + str(len(sequences)) + " image sequences")
    return True


def center_img(sequence):
    """
    Takes a single img strip and centers it on the screen.
    If the img is the same ratio as the render output, the function returns.
    Else it sets the strip to use the image offset and centers it.

    Returns false if it couldn't complete, otherwise True.
    """
    # DOESN'T TAKE IN ACCOUNT IMAGE CROP
    if sequence.use_translation and (sequence.transform.offset_x != 0 or
                                     sequence.transform.offset_y != 0):
        return False

    image_width = sequence.elements[0].orig_width
    image_height = sequence.elements[0].orig_height
    if image_width == 0 or image_height == 0:
        raise ZeroDivisionError('image_height or image_width is 0')

    render = bpy.context.scene.render
    res_x, res_y = render.resolution_x, render.resolution_y
    image_ratio = image_width / image_height
    render_ratio = res_x / res_y
    if image_ratio == render_ratio:
        return False

    if image_width < res_x or image_height < res_y:
        sequence.use_translation = True
        sequence.transform.offset_x = (res_x - image_width) / 2
        sequence.transform.offset_y = (res_y - image_height) / 2
    return True