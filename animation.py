"""Operators that add animation to the sequences
   These can include fades, transforms, etc."""
import bpy
from bpy.props import BoolProperty, IntProperty, EnumProperty
from .functions.sequences import SequenceTypes


def fade_find_fcurve(sequence=None):
    """
    Checks if there's a fade animation on a single sequence
    If the right fcurve is found,
    volume for audio sequences and blend_alpha for other sequences,
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


# TODO: Use a handler to auto move the fades with extend 
# and the strips' handles
class FadeStrips(bpy.types.Operator):
    bl_idname = "power_sequencer.fade_strips"
    bl_label = "PS - Fade strips"
    bl_description = "Fade left, right or both sides of all selected strips \
                      in the VSE"

    bl_options = {'REGISTER', 'UNDO'}

    fade_length = IntProperty(name="Fade length",
                              description="Length of the fade in frames",
                              default=12,
                              min=1)
    fade_type = EnumProperty(
        items=[('both', 'Fade in and out', 'Fade selected strips in and out'),
               ('left', 'Fade in', 'Fade in selected strips'), (
                   'right', 'Fade out', 'Fade out selected strips')],
        name="Fade type",
        description="Fade in, out, or both in and out. Default is both.",
        default='both')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = bpy.context.scene
        selection = bpy.context.selected_sequences
        if not selection:
            return {"CANCELLED"}

        fade_sequence_count = 0
        for s in selection:
            max_value = s.volume if s.type in SequenceTypes.SOUND \
                        else s.blend_alpha
            if not max_value:
                max_value = 1.0

            # Create animation data and an action if there is none in the scene
            if scene.animation_data is None:
                scene.animation_data_create()
            if scene.animation_data.action is None:
                action = bpy.data.actions.new(scene.name + "Action")
                scene.animation_data.action = action

            # Create fade
            fcurves = bpy.context.scene.animation_data.action.fcurves

            fade_clear(s)
            frame_start, frame_end = s.frame_final_start, s.frame_final_end

            fade_in_frames = (frame_start, frame_start + self.fade_length)
            fade_out_frames = (frame_end - self.fade_length, frame_end)

            fade_fcurve, fade_curve_type = fade_find_fcurve(s)
            if fade_fcurve is None:
                fade_fcurve = fcurves.new(data_path=s.path_from_id(fade_curve_type))

            min_length = self.fade_length * 2 if self.fade_type == 'both' else self.fade_length
            if not s.frame_final_duration > min_length:
                continue

            keys = fade_fcurve.keyframe_points
            if self.fade_type in ['left', 'both']:
                keys.insert(frame=frame_start, value=0)
                keys.insert(frame=frame_start + self.fade_length, value=max_value)
            if self.fade_type in ['right', 'both']:
                keys.insert(frame=frame_end - self.fade_length, value=max_value)
                keys.insert(frame=frame_end, value=0)
            fade_sequence_count += 1

        self.report({"INFO"}, "Added fade animation to {!s} sequences.".format(fade_sequence_count))
        return {"FINISHED"}


class AddTransformEffect(bpy.types.Operator):
    """
    Filters the selection down to image and movie strips
    Centers the pivot point of image strips.
    Adds a transform effect and sets it to ALPHA_OVER
    for each strip in the selection.
    """
    bl_idname = 'power_sequencer.add_transform_effect'
    bl_label = 'PS - Add transform effect'
    bl_description = 'Add transform effect to selected image and movie strips. \
                      Auto centers images'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        sequence_editor = bpy.context.scene.sequence_editor
        render = bpy.context.scene.render
        scene = bpy.context.scene

        selection = bpy.context.selected_sequences
        selection = [s for s in selection if s.type in ('IMAGE', 'MOVIE')]
        if not selection:
            self.report({"ERROR_INVALID_INPUT"},
                        "No sequences movie or image strips selected")
            return {'CANCELLED'}

        transform_strips = []
        sequencer.select_all(action='DESELECT')
        image_strips = [s for s in selection if s.type == 'IMAGE']

        # Center image strips pivot
        for s in image_strips:
            if s.use_translation and (s.transform.offset_x != 0 or
                                      s.transform.offset_y != 0):
                continue
            
            image_width = s.elements[0].orig_width
            image_height = s.elements[0].orig_height
            if image_width == 0 or image_height == 0:
                raise ValueError('image_height or image_width is 0')

            # image_ratio = image_width / image_height
            # render_ratio = render.resolution_x / render.resolution_y
            # if image_ratio != render_ratio:
            #     continue

            if image_width < render.resolution_x or image_height < render.resolution_y:
                s.use_translation = True
                s.transform.offset_x = (render.resolution_x - image_width) / 2
                s.transform.offset_y = (render.resolution_y - image_height) / 2

        # Add a transform effect to all selected MOVIE and IMAGE strips
        for s in selection:
            sequence_editor.active_strip = s
            sequencer.effect_strip_add(type='TRANSFORM')

            active = sequence_editor.active_strip
            active.name = "TRANSFORM-{!s}".format(s.name)
            active.blend_type = 'ALPHA_OVER'
            transform_strips.append(active)
            active.select = False
            s.mute = True

        # Select img strips and transform effects
        for s in transform_strips:
            s.select = True
        for s in selection:
            s.select = True
        sequence_editor.active_strip = transform_strips[0]
        self.report({"INFO"}, "Successfully processed " + str(len(selection)) +
                    " image sequences")
        return {'FINISHED'}


# TODO: Find which animation data to store and how to store it?
# class AddAnimationFromLibrary(bpy.types.Operator):
#     bl_idname = "power_sequencer.animation_library"
#     bl_label = "PS - Animation library"
#     bl_description = "Adds animation to selected strips."
#     bl_options = {"REGISTER", "UNDO"}

#     both_sides = BoolProperty(
#         name="Both sides",
#         description="Animate both the start and the end of the strip",
#         default=True)
#     # TODO: Get the presets from a subfolder/file
#     presets = None

#     @classmethod
#     def poll(cls, context):
#         return context.selected_sequences

#     def execute(self, context):
#         sequencer = bpy.ops.sequencer
#         return {"FINISHED"}
