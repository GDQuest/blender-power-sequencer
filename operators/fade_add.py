import bpy

from .utils.convert_duration_to_frames import convert_duration_to_frames
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


# TODO: Use a handler to auto move the fades with extend
# and the strips' handles
class POWER_SEQUENCER_OT_fade_add(bpy.types.Operator):
    """
    Animate a strips opacity to zero. By default, the duration of the fade is 0.5 seconds
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': 'https://i.imgur.com/XoUM2vw.gif',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'F', 'value': 'PRESS', 'alt': True}, {'fade_type': 'RIGHT'}, 'Fade Right'),
            ({'type': 'F', 'value': 'PRESS', 'ctrl': True}, {'fade_type': 'LEFT'}, 'Fade Left'),
            ({'type': 'F', 'value': 'PRESS'}, {'fade_type': 'BOTH'}, 'Fade Both')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    fade_duration: bpy.props.FloatProperty(
        name="Fade Duration",
        description="Duration of the fade in seconds",
        default=0.5,
        min=0)
    fade_type: bpy.props.EnumProperty(
        items=[('BOTH', 'Fade in and out', 'Fade selected strips in and out'),
               ('LEFT', 'Fade in', 'Fade in selected strips'),
               ('RIGHT', 'Fade out', 'Fade out selected strips')],
        name="Fade type",
        description="Fade in, out, or both in and out. Default is both",
        default='BOTH')

    time_cursor_frame_start = -1
    animated_property = ''

    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def execute(self, context):
        scene = context.scene
        fcurves = scene.animation_data.action.fcurves

        self.fade_length = convert_duration_to_frames(context, self.fade_duration)

        # Create a scene action if there's none
        if not scene.animation_data:
            scene.animation_data_create()
        if not scene.animation_data.action:
            action = bpy.data.actions.new(scene.name + "Action")
            scene.animation_data.action = action

        faded_sequences = []
        for sequence in context.selected_sequences:
            self.animated_property = 'volume' if hasattr(sequence, 'volume') else 'blend_alpha'
            max_value = getattr(sequence, self.animated_property, 1.0)

            # Create fade
            self.fade_animation_remove(context, sequence)

            fade_fcurve = self.fade_find_fcurve(context, sequence)
            if not fade_fcurve:
                fade_fcurve = fcurves.new(data_path=sequence.path_from_id(self.animated_property))

            minimum_duration = (self.fade_length * 2
                                if self.fade_type == 'BOTH' else
                                self.fade_length)
            if not sequence.frame_final_duration >= minimum_duration:
                continue

            keys = fade_fcurve.keyframe_points
            if self.fade_type in ['LEFT', 'BOTH']:
                keys.insert(frame=sequence.frame_final_start, value=0.0)
                keys.insert(frame=sequence.frame_final_start + self.fade_length, value=max_value)
            if self.fade_type in ['RIGHT', 'BOTH']:
                keys.insert(frame=sequence.frame_final_end - self.fade_length, value=max_value)
                keys.insert(frame=sequence.frame_final_end, value=0.0)
            faded_sequences.append(sequence)

        self.report({"INFO"}, "Added fade animation to {} sequences.".format(len(faded_sequences)))
        return {"FINISHED"}

    def fade_find_fcurve(self, context, sequence):
        """
        Iterates over all the fcurves until it finds an fcurve with a data path
        that corresponds to the sequence.
        Returns the matching FCurve or None if the function can't find a match.
        """
        fade_fcurve = None
        fcurves = context.scene.animation_data.action.fcurves
        for fcurve in fcurves:
            if (fcurve.data_path == 'sequence_editor.sequences_all["' +
                    sequence.name + '"].' + self.animated_property):
                fade_fcurve = fcurve
                break
        return fade_fcurve

    def fade_animation_remove(self, context, sequence):
        """
        Deletes all keyframes in the blend_alpha
        or volume fcurve of the provided sequence
        """
        if not sequence:
            raise AttributeError('Missing sequence parameter')

        fcurves = context.scene.animation_data.action.fcurves
        fade_fcurve = self.fade_find_fcurve(context, sequence)
        if fade_fcurve:
            fcurves.remove(fade_fcurve)
