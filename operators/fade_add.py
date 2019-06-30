import bpy
from mathutils import Vector

from .utils.convert_duration_to_frames import convert_duration_to_frames
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_fade_add(bpy.types.Operator):
    """
    *brief* Animate a strip's opacity to zero.

    By default, the duration of the fade is 0.5 seconds
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': 'https://i.imgur.com/XoUM2vw.gif',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'F', 'value': 'PRESS', 'alt': True}, {'type': 'OUT'}, 'Fade Right'),
            ({'type': 'F', 'value': 'PRESS', 'ctrl': True}, {'type': 'IN'}, 'Fade Left'),
            ({'type': 'F', 'value': 'PRESS'}, {'type': 'IN_OUT'}, 'Fade Both')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    duration_seconds: bpy.props.FloatProperty(
        name="Fade Duration",
        description="Duration of the fade in seconds",
        default=1.0,
        min=0.0)
    type: bpy.props.EnumProperty(
        items=[('IN_OUT', 'Fade in and out', 'Fade selected strips in and out'),
               ('IN', 'Fade in', 'Fade in selected strips'),
               ('OUT', 'Fade out', 'Fade out selected strips')],
        name="Fade type",
        description="Fade in, out, or both in and out. Default is both",
        default='IN_OUT')

    # list of Fade objects, mutates for every sequence
    fades = []

    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def execute(self, context):
        scene = context.scene
        fcurves = scene.animation_data.action.fcurves

        # We must create a scene action first if there's none
        if not scene.animation_data:
            scene.animation_data_create()
        if not scene.animation_data.action:
            action = bpy.data.actions.new(scene.name + "Action")
            scene.animation_data.action = action

        faded_sequences = []
        for sequence in context.selected_sequences:
            self.fades = self.calculate_fades(sequence)

            if not self.is_long_enough(sequence):
                continue

            self.fade_fcurve = self.fade_find_or_create_fcurve(context, sequence)
            self.fade_animation_clear(context)
            self.fade_animation_create()
            faded_sequences.append(sequence)

        self.report({"INFO"}, "Added fade animation to {} sequences.".format(len(faded_sequences)))
        return {"FINISHED"}

    def is_long_enough(self, sequence):
        duration_frames = self.fades[0].duration_frames
        minimum_duration = (duration_frames * 2
                            if self.type == 'IN_OUT' else
                            duration_frames)
        return sequence.frame_final_duration >= minimum_duration

    def calculate_fades(self, sequence):
        """
        Returns a list of Fade objects
        """
        fades = []
        if self.type in ['IN', 'IN_OUT']:
            fade = Fade(sequence, 'IN', self.duration_seconds)
            fades.append(fade)
        if self.type in ['OUT', 'IN_OUT']:
            fade = Fade(sequence, 'OUT', self.duration_seconds)
            fades.append(fade)
        return fades

    def fade_find_or_create_fcurve(self, context, sequence):
        """
        Iterates over all the fcurves until it finds an fcurve with a data path
        that corresponds to the sequence.
        Returns the matching FCurve or creates a new one if the function can't find a match.
        """
        fade_fcurve = None
        fcurves = context.scene.animation_data.action.fcurves
        prop = self.fades[0].animated_property
        searched_data_path = sequence.path_from_id(prop)
        for fcurve in fcurves:
            if fcurve.data_path == searched_data_path:
                fade_fcurve = fcurve
                break
        if not fade_fcurve:
            fade_fcurve = fcurves.new(data_path=searched_data_path)
        return fade_fcurve

    def fade_animation_clear(self, context):
        """
        Removes existing keyframes in the fades' time range
        """
        keyframe_points = self.fade_fcurve.keyframe_points
        for keyframe in keyframe_points:
            frame = keyframe.co[0]
            for fade in self.fades:
                if fade.start.x < frame < fade.end.x:
                    keyframe_points.remove(keyframe)

    def fade_animation_create(self):
        for fade in self.fades:
            for point in (fade.start, fade.end):
                self.fade_fcurve.keyframe_points.insert(frame=point.x, value=point.y)


class Fade:
    """
    Data structure to represent fades
    """
    type = ''
    animated_property = ''
    duration_frames = -1
    start, end = Vector((0, 0)), Vector((0, 0))

    def __init__(self, sequence, type, duration_seconds):
        self.type = type
        self.animated_property = 'volume' if hasattr(sequence, 'volume') else 'blend_alpha'
        self.duration_frames = convert_duration_to_frames(bpy.context, duration_seconds)

        max_value = self.calculate_max_value(sequence)
        if type == 'IN':
            self.start = Vector((sequence.frame_final_start, 0.0))
            self.end = Vector((sequence.frame_final_start + self.duration_frames, max_value))
        elif type == 'OUT':
            self.start = Vector((sequence.frame_final_end - self.duration_frames, max_value))
            self.end = Vector((sequence.frame_final_end, 0.0))

    def calculate_max_value(self, sequence):
        """
        Returns the maximum Y coordinate the fade animation should use for a given sequence
        """
        # Using the current value or 1.0 for the fade's maximum
        # TODO: use the highest point in the curve?
        max_value = getattr(sequence, self.animated_property, 1.0)
        max_value = max_value if max_value > 0.0 else 1.0
        max_value = 1.0
        return max_value
