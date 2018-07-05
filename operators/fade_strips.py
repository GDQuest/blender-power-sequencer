import bpy
from .utils.global_settings import SequenceTypes
from .utils.convert_duration_to_frames import convert_duration_to_frames


# TODO: Use a handler to auto move the fades with extend
# and the strips' handles
class FadeStrips(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/XoUM2vw.gif)

    Animate a strips opacity to zero. By default, the duration of the
    fade is 0.5 seconds.
    """
    bl_idname = "power_sequencer.fade_strips"
    bl_label = "Fade Strips"
    bl_description = "Fade left, right or both sides of all selected strips in the VSE"

    bl_options = {'REGISTER', 'UNDO'}

    fade_duration = bpy.props.FloatProperty(
        name="Fade Duration",
        description="The Duration of the Fade",
        default=0.5,
        min=0)
    fade_type = bpy.props.EnumProperty(
        items=[('both', 'Fade in and out', 'Fade selected strips in and out'),
               ('left', 'Fade in', 'Fade in selected strips'),
               ('right', 'Fade out', 'Fade out selected strips')],
        name="Fade type",
        description="Fade in, out, or both in and out. Default is both.",
        default='both')

    current_frame = None

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = bpy.context.scene
        self.fade_length = convert_duration_to_frames(self.fade_duration)

        # Because of the way blender updates opacity, it's best if the
        # CTI is not on any strip while adding these keyframes.
        # We put the CTI back afterward
        self.current_frame = scene.frame_current
        all_strips = sorted(
            scene.sequence_editor.sequences_all,
            key=lambda s: s.frame_final_end)
        last_frame = all_strips[-1].frame_final_end
        scene.frame_current = last_frame + 1

        selection = bpy.context.selected_sequences
        if not selection:
            return {"CANCELLED"}

        fade_sequence_count = 0
        for s in selection:

            max_value = s.volume if s.type in SequenceTypes.SOUND else s.blend_alpha
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

            self.fade_clear(s)
            frame_start, frame_end = s.frame_final_start, s.frame_final_end

            # fade_in_frames = (frame_start, frame_start + self.fade_length)
            # fade_out_frames = (frame_end - self.fade_length, frame_end)

            fade_fcurve, fade_curve_type = self.fade_find_fcurve(s)
            if fade_fcurve is None:
                fade_fcurve = fcurves.new(
                    data_path=s.path_from_id(fade_curve_type))

            min_length = self.fade_length * 2 if self.fade_type == 'both' else self.fade_length
            if not s.frame_final_duration > min_length:
                continue

            keys = fade_fcurve.keyframe_points
            if self.fade_type in ['left', 'both']:
                keys.insert(frame=frame_start, value=0)
                keys.insert(
                    frame=frame_start + self.fade_length, value=max_value)
            if self.fade_type in ['right', 'both']:
                keys.insert(
                    frame=frame_end - self.fade_length, value=max_value)
                keys.insert(frame=frame_end, value=0)
            fade_sequence_count += 1

            # We toggle this to help with updating the opacity change
            s.mute = not s.mute
            s.mute = not s.mute

        scene.frame_current = self.current_frame

        self.report({"INFO"}, "Added fade animation to {!s} sequences.".format(
            fade_sequence_count))
        return {"FINISHED"}

    def fade_find_fcurve(self, sequence=None):
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
            if (fc.data_path == 'sequence_editor.sequences_all["' +
                    sequence.name + '"].' + fade_type):
                fade_fcurve = fc
                break
        return fade_fcurve, fade_type

    def fade_clear(self, sequence=None):
        """
        Deletes all keyframes in the blend_alpha
        or volume fcurve of the provided sequence
        """
        if not sequence:
            raise AttributeError('Missing sequence parameter')

        fcurves = bpy.context.scene.animation_data.action.fcurves
        fade_fcurve = self.fade_find_fcurve(sequence)[0]
        if fade_fcurve:
            fcurves.remove(fade_fcurve)
