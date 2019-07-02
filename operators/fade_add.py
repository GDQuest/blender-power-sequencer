import bpy
from mathutils import Vector
from math import floor

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_fade_add(bpy.types.Operator):
    """*brief* Adds or updates a fade animation for either visual or audio strips.

    Fade options:

    - In, Out, In and Out create a fade animation of the given duration from
    the start of the sequence, to the end of the sequence, or on boths sides
    - From playhead: the fade animation goes from the start of sequences under the playhead to the playhead
    - To playhead: the fade animation goes from the playhead to the end of sequences under the playhead

    By default, the duration of the fade is 1 second.
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': 'https://i.imgur.com/XoUM2vw.gif',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'F', 'value': 'PRESS', 'alt': True}, {'type': 'OUT'}, 'Fade Out'),
            ({'type': 'F', 'value': 'PRESS', 'ctrl': True}, {'type': 'IN'}, 'Fade In'),
            ({'type': 'F', 'value': 'PRESS'}, {'type': 'IN_OUT'}, 'Fade In and Out')
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
               ('OUT', 'Fade out', 'Fade out selected strips'),
               ('CURSOR_FROM', 'From playhead', 'Fade from the time cursor to the end of overlapping sequences'),
               ('CURSOR_TO', 'To playhead', 'Fade from the start of sequences under the time cursor to the current frame')],
        name="Fade type",
        description="Fade in, out, or both in and out. Default is both",
        default='IN_OUT')

    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def execute(self, context):
        # We must create a scene action first if there's none
        scene = context.scene
        if not scene.animation_data:
            scene.animation_data_create()
        if not scene.animation_data.action:
            action = bpy.data.actions.new(scene.name + "Action")
            scene.animation_data.action = action

        sequences = context.selected_sequences
        if self.type in ['CURSOR_TO', 'CURSOR_FROM']:
            sequences = [s for s in sequences
                         if s.frame_final_start < context.scene.frame_current < s.frame_final_end]

        max_duration = min(sequences, key=lambda s: s.frame_final_duration).frame_final_duration
        max_duration = floor(max_duration / 2.0) if self.type == 'IN_OUT' else max_duration

        faded_sequences = []
        for sequence in sequences:
            duration = self.calculate_fade_duration(context, sequence)
            duration = min(duration, max_duration)
            if not self.is_long_enough(sequence, duration):
                continue

            animated_property = 'volume' if hasattr(sequence, 'volume') else 'blend_alpha'
            fade_fcurve = fade_find_or_create_fcurve(context, sequence, animated_property)
            max_value = fade_calculate_max_value(sequence, fade_fcurve)
            fades = self.calculate_fades(sequence, animated_property, duration, max_value)
            fade_animation_clear(context, fade_fcurve, fades)
            fade_animation_create(fade_fcurve, fades)
            faded_sequences.append(sequence)

        sequence_string = "sequence" if len(faded_sequences) == 1 else "sequences"
        self.report({"INFO"}, "Added fade animation to {} {}.".format(len(faded_sequences), sequence_string))
        return {"FINISHED"}

    def calculate_fade_duration(self, context, sequence):
        frame_current = context.scene.frame_current
        duration = 0.0
        if self.type == 'CURSOR_TO':
            duration = abs(frame_current - sequence.frame_final_start)
        elif self.type == 'CURSOR_FROM':
            duration = abs(sequence.frame_final_end - frame_current)
        else:
            duration = calculate_duration_frames(context, self.duration_seconds)
        return duration

    def is_long_enough(self, sequence, duration=0.0):
        minimum_duration = (duration * 2
                            if self.type == 'IN_OUT' else
                            duration)
        return sequence.frame_final_duration >= minimum_duration

    def calculate_fades(self, sequence, animated_property, duration, max_value):
        """
        Returns a list of Fade objects
        """
        fades = []
        if self.type in ['IN', 'IN_OUT', 'CURSOR_TO']:
            fade = Fade(sequence, 'IN', animated_property, duration, max_value)
            fades.append(fade)
        if self.type in ['OUT', 'IN_OUT', 'CURSOR_FROM']:
            fade = Fade(sequence, 'OUT', animated_property, duration, max_value)
            fades.append(fade)
        return fades


def fade_find_or_create_fcurve(context, sequence, animated_property):
    """
    Iterates over all the fcurves until it finds an fcurve with a data path
    that corresponds to the sequence.
    Returns the matching FCurve or creates a new one if the function can't find a match.
    """
    fade_fcurve = None
    fcurves = context.scene.animation_data.action.fcurves
    searched_data_path = sequence.path_from_id(animated_property)
    for fcurve in fcurves:
        if fcurve.data_path == searched_data_path:
            fade_fcurve = fcurve
            break
    if not fade_fcurve:
        fade_fcurve = fcurves.new(data_path=searched_data_path)
    return fade_fcurve


def fade_calculate_max_value(sequence, fade_fcurve):
    """
    Returns the maximum Y coordinate the fade animation should use for a given sequence
    """
    property = fade_fcurve.data_path.rsplit('.', 1)[-1]
    if not fade_fcurve.keyframe_points:
        max_value = getattr(sequence, property, 1.0)
    else:
        highest_keyframe = max(fade_fcurve.keyframe_points, key=lambda k: k.co[1])
        max_value = highest_keyframe.co[1]
    max_value = max_value if max_value > 0.0 else 1.0
    return max_value


def fade_animation_clear(context, fade_fcurve, fades):
    """
    Removes existing keyframes in the fades' time range, in fast mode, without
    updating the fcurve
    """
    keyframe_points = fade_fcurve.keyframe_points
    for keyframe in keyframe_points:
        frame = keyframe.co[0]
        for fade in fades:
            if fade.start.x < frame < fade.end.x:
                keyframe_points.remove(keyframe, fast=True)


def fade_animation_create(fade_fcurve, fades):
    """
    Inserts keyframes in the fade_fcurve in fast mode using the Fade objects.
    Updates the fcurve after having inserted all keyframes to finish the animation.
    """
    keyframe_points = fade_fcurve.keyframe_points
    for fade in fades:
        for point in (fade.start, fade.end):
            keyframe_points.insert(frame=point.x, value=point.y, options={'FAST'})
    fade_fcurve.update()
    # The graph editor and the audio waveforms only redraw upon "moving" a keyframe
    keyframe_points[-1].co = keyframe_points[-1].co


class Fade:
    """
    Data structure to represent fades
    """
    type = ''
    animated_property = ''
    duration = -1
    max_value = 1.0
    start, end = Vector((0, 0)), Vector((0, 0))

    def __init__(self, sequence, type, animated_property, duration, max_value):
        self.type = type
        self.animated_property = animated_property
        self.duration = duration
        self.max_value = max_value

        if type == 'IN':
            self.start = Vector((sequence.frame_final_start, 0.0))
            self.end = Vector((sequence.frame_final_start + self.duration, max_value))
        elif type == 'OUT':
            self.start = Vector((sequence.frame_final_end - self.duration, max_value))
            self.end = Vector((sequence.frame_final_end, 0.0))

    def __repr__(self):
        return "Fade {}: {} to {}".format(self.type, self.start, self.end)


def calculate_duration_frames(context, duration_seconds):
    return round(duration_seconds * context.scene.render.fps / context.scene.render.fps_base)
