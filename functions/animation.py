"""Functions related to animation data like fades, transform, masks., etc."""
import bpy
from .global_settings import SequenceTypes


def fade_create(sequences=None, fade_length=12, fade_type='both'):
    """Takes a list of sequences, and adds a fade to the left,
       right or to both sides of the VSE strips.
       fade_length: length of the fade in frames
       fade_type: 'left', 'right' or 'both' """

    if not sequences:
        return None

    scene = bpy.context.scene

    if scene.animation_data is None:
        scene.animation_data_create()
    if scene.animation_data.action is None:
        action = bpy.data.actions.new(scene.name + "Action")
        scene.animation_data.action = action

    fcurves = scene.animation_data.action.fcurves

    # TODO: Detect existing fades and don't delete every time
    fade_clear(sequences)

    for s in sequences:
        s_start = s.frame_final_start
        s_end = s.frame_final_end

        fade_in_frames = (s_start, s_start + fade_length)
        fade_out_frames = (s_end - fade_length, s_end)

        # TODO: Currently, the fades are always cleared, so fade_find_fcurve
        # will always return None, but it does return fade_type, which we need.
        fade_fcurve, fade_curve_type = fade_find_fcurve(s)
        if fade_fcurve is None:
            fade_fcurve = fcurves.new(data_path=s.path_from_id(fade_curve_type))

        min_length = fade_length * 2 if fade_type == 'both' else fade_length
        if not s.frame_final_duration > min_length:
            print(s.name + ' is too short for the fade to be applied.')
            continue

        # TODO: give the option to use the fade_curve's highest value
        # or strip value
        fade_max_value = 1
        keys = fade_fcurve.keyframe_points
        # ADDING KEYFRAMES
        if fade_type in ['left', 'both']:
            keys.insert(frame=fade_in_frames[0], value=0)
            keys.insert(frame=fade_in_frames[1], value=fade_max_value)
        if fade_type in ['right', 'both']:
            keys.insert(frame=fade_out_frames[0], value=fade_max_value)
            keys.insert(frame=fade_out_frames[1], value=0)
    return len(sequences)


def fade_find_fcurve(sequence=None):
    """Checks if there's existing fade animation on a given video sequence.
    If so, returns the data path to the corresponding fcurve.
    Also returns the strip's fade type"""

    fcurves = bpy.context.scene.animation_data.action.fcurves

    if sequence:
        if sequence.type in SequenceTypes.SOUND:
            fade_type = 'volume'
        else:
            fade_type = 'blend_alpha'

        fade_fcurve = None
        for c in fcurves:
            if (c.data_path == 'sequence_editor.sequences_all["' + sequence.name + '"].' + fade_type):
                fade_fcurve = c
                break
    return fade_fcurve, fade_type


def fade_clear(sequences=None):
    """Deletes all keyframes in the blend_alpha
    or volume fcurves of the provided sequences"""
    if not sequences:
        return None

    fcurves = bpy.context.scene.animation_data.action.fcurves

    for s in sequences:
        fade_fcurve = fade_find_fcurve(s)[0]
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

        sequence_editor.active_strip = s
        sequencer.effect_strip_add(type='TRANSFORM')

        active = sequence_editor.active_strip
        active.name = "TRANSFORM-%s" % s.name
        active.blend_type = 'ALPHA_OVER'
        active.select = False

    print("Successfully processed " + str(len(sequences)) +
          " image sequences")
    return True


# def calc_transform_effect_scale(sequence):
#     """Takes a transform effect and returns the scale it should use
#        to preserve the scale of its cropped input"""
#     # if not (sequence or sequence.type == 'TRANSFORM'):
#     #     raise AttributeError

#     s = sequence.input_1

#     crop_x, crop_y = s.elements[0].orig_width - (s.crop.min_x + s.crop.max_x),
#                      s.elements[0].orig_height - (s.crop.min_y + s.crop.max_y)
#     ratio_x, ratio_y = crop_x / render.resolution_x,
#                        crop_y / render.resolution_y
#     if ratio_x > 1 or ratio_y > 1:
#         ratio_x /= ratio_y
#         ratio_y /= ratio_x
#     return ratio_x, ratio_y
#     active.scale_start_x, active.scale_start_y = ratio_x ratio_y

