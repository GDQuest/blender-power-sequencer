"""Functions related to animation data like fades, transform, masks., etc."""
import bpy
from .global_settings import SequenceTypes


# TODO: Detect existing fades and don't delete every time
# TODO: Use a handler to auto move the fades with extend and the strips' handles
def fade_create(sequence=None,
                fade_length=12,
                fade_type='both',
                max_value=1.0):
    """
    Takes a single sequence, and adds a fade to the left,
    right or to both sides of the VSE strips.

    Args:
    fade_length: length of the fade in frames
    fade_type: 'left', 'right' or 'both'
    """
    if not sequence:
        return None

    print("in function", max_value)
    create_animation_data()
    fcurves = bpy.context.scene.animation_data.action.fcurves

    s = sequence
    fade_clear(s)
    frame_start, frame_end = s.frame_final_start, s.frame_final_end

    fade_in_frames = (frame_start, frame_start + fade_length)
    fade_out_frames = (frame_end - fade_length, frame_end)

    fade_fcurve, fade_curve_type = fade_find_fcurve(s)
    if fade_fcurve is None:
        fade_fcurve = fcurves.new(data_path=s.path_from_id(fade_curve_type))

    min_length = fade_length * 2 if fade_type == 'both' else fade_length
    if not s.frame_final_duration > min_length:
        return s.name + ' is too short for the fade to be applied.'

    keys = fade_fcurve.keyframe_points
    if fade_type in ['left', 'both']:
        keys.insert(frame=frame_start, value=0)
        keys.insert(frame=frame_start + fade_length, value=max_value)
    if fade_type in ['right', 'both']:
        keys.insert(frame=frame_end - fade_length, value=max_value)
        keys.insert(frame=frame_end, value=0)
    return s.name


def create_animation_data():
    """
    Creates animation data and an action if there is none in the scene
    """
    scene = bpy.context.scene

    if scene.animation_data is None:
        scene.animation_data_create()
    if scene.animation_data.action is None:
        action = bpy.data.actions.new(scene.name + "Action")
        scene.animation_data.action = action
    return True


def fade_find_fcurve(sequence=None):
    """
    Checks if there's a fade animation on a single sequence
    If the right fcurve is found (volume for audio sequences and blend_alpha for other sequences),

    Returns a tuple of (fade_fcurve, fade_type)
    """
    fcurves = bpy.context.scene.animation_data.action.fcurves
    if not sequence:
        raise AttributeError('Missing sequence parameter')

    fade_fcurve = None
    fade_type = 'volume' if sequence.type in SequenceTypes.SOUND else 'blend_alpha'
    for fc in fcurves:
        if (fc.data_path == 'sequence_editor.sequences_all["' + sequence.name +
                '"].' + fade_type):
            fade_fcurve = fc
            break
    return fade_fcurve, fade_type


def fade_clear(sequence=None):
    """
    Deletes all keyframes in the blend_alpha
    or volume fcurve of the provided sequence
    """
    if not sequence:
        raise AttributeError('Missing sequence parameter')

    fcurves = bpy.context.scene.animation_data.action.fcurves
    fade_fcurve = fade_find_fcurve(sequence)[0]
    if fade_fcurve:
        fcurves.remove(fade_fcurve)
    return True


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