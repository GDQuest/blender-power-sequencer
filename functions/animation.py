"""Functions related to animation data like fades, transform, masks., etc."""
import bpy
from .global_settings import SequenceTypes


# TODO: Detect existing fades and don't delete every time
# TODO: Use a handler to auto move the fades with extend and the strips' handles
def fade_create(sequence=None,
                fade_length=12,
                fade_type='both',
                max_opacity=1.0):
    """
    Takes a single sequence, and adds a fade to the left,
    right or to both sides of the VSE strips.

    Args:
    fade_length: length of the fade in frames
    fade_type: 'left', 'right' or 'both'
    """
    if not sequence:
        return None

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
        keys.insert(frame=frame_start + fade_length, value=max_opacity)
    if fade_type in ['right', 'both']:
        keys.insert(frame=frame_end - fade_length, value=max_opacity)
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
    """
    Takes a list of image strips and adds a transform effect to them.
    Ensures that the pivot will be centered on the image
    """
    sequences = [s for s in sequences if s.type in ('IMAGE', 'MOVIE')]
    if not sequences:
        return None

    sequencer = bpy.ops.sequencer
    sequence_editor = bpy.context.scene.sequence_editor

    sequencer.select_all(action='DESELECT')
    for s in sequences:
        s.mute = True

        sequence_editor.active_strip = s
        sequencer.effect_strip_add(type='TRANSFORM')

        active = sequence_editor.active_strip
        active.name = "TRANSFORM-%s" % s.name
        active.blend_type = 'ALPHA_OVER'
        active.select = False

    print("Successfully processed " + str(len(sequences)) + " image sequences")
    return True


# def calc_transform_effect_scale(sequence=None):
#     """
#     Takes a transform effect and returns the scale it should use
#     to preserve the scale of its cropped input
#     """
#     if not (sequence or sequence.type == 'TRANSFORM'):
#         raise AttributeError('Missing sequence parameter or sequence is not of type TRANSFORM')

#     source = sequence.input_1

#     crop_x = source.elements[0].orig_width - (source.crop.min_x + source.crop.max_x)
#     crop_y = source.elements[0].orig_height - (source.crop.min_y + source.crop.max_y)

#     ratio_x = crop_x / render.resolution_x
#     ratio_y = crop_y / render.resolution_y

#     if ratio_x > 1 or ratio_y > 1:
#         ratio_x /= ratio_y
#         ratio_y /= ratio_x
#     # active.scale_start_x, active.scale_start_y = ratio_x ratio_y
#     return ratio_x, ratio_y
