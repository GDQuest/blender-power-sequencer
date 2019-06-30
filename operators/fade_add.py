import bpy
from mathutils import Vector

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

    # The properties below mutate for every sequence to apply fades to
    animated_property = ''
    # list of Vector()
    fade_ranges = []

    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def execute(self, context):
        scene = context.scene
        fcurves = scene.animation_data.action.fcurves

        self.fade_length = convert_duration_to_frames(context, self.fade_duration)

        # We must create a scene action first if there's none
        if not scene.animation_data:
            scene.animation_data_create()
        if not scene.animation_data.action:
            action = bpy.data.actions.new(scene.name + "Action")
            scene.animation_data.action = action

        faded_sequences = []
        for sequence in context.selected_sequences:
            if not self.is_long_enough(sequence):
                continue

            self.animated_property = 'volume' if hasattr(sequence, 'volume') else 'blend_alpha'
            self.max_value = self.calculate_max_value(sequence)
            self.fade_ranges = self.calculate_fade_ranges(sequence)

            self.fade_fcurve = self.fade_find_fcurve(context, sequence)
            if not self.fade_fcurve:
                self.fade_fcurve = fcurves.new(data_path=sequence.path_from_id(self.animated_property))

            self.fade_animation_clear(context, sequence)
            self.fade_animation_create()
            faded_sequences.append(sequence)

        self.report({"INFO"}, "Added fade animation to {} sequences.".format(len(faded_sequences)))
        return {"FINISHED"}

    def is_long_enough(self, sequence):
        minimum_duration = (self.fade_length * 2
                            if self.fade_type == 'BOTH' else
                            self.fade_length)
        return sequence.frame_final_duration >= minimum_duration

    def calculate_fade_ranges(self, sequence):
        """
        Returns a dictionary of 1 or 2 tuples of Vectors that represent coordinates to key for fade animations
        The dictionary has the form {'IN': (start:Vector, end:Vector), 'OUT': (...)} with each key being optional
        """
        ranges = {}
        if self.fade_type in ['LEFT', 'BOTH']:
            point_start = Vector((sequence.frame_final_start, 0.0))
            point_end = Vector((sequence.frame_final_start + self.fade_length, self.max_value))
            ranges['IN'] = (point_start, point_end)
        if self.fade_type in ['RIGHT', 'BOTH']:
            point_start = Vector((sequence.frame_final_end - self.fade_length, self.max_value))
            point_end = Vector((sequence.frame_final_end, 0.0))
            ranges['OUT'] = (point_start, point_end)
        return ranges

    def calculate_max_value(self, sequence):
        """
        Returns the maximum Y coordinate the fade animation should use for a given sequence
        """
        # Using the current value or 1.0 for the fade's maximum
        # TODO: use the highest point in the curve?
        max_value = getattr(sequence, self.animated_property, 1.0)
        max_value = max_value if max_value > 0.0 else 1.0
        return max_value

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

    def fade_animation_clear(self, context, sequence):
        """
        Removes existing keyframes in the fades' time range
        """
        keyframe_points = self.fade_fcurve.keyframe_points
        for keyframe in keyframe_points:
            frame = keyframe.co[0]
            for fade_range in self.fade_ranges.values():
                if fade_range[0].x <= frame <= fade_range[1].x:
                    keyframe_points.remove(keyframe)

    def fade_animation_create(self):
        for fade_range in self.fade_ranges.values():
            for point in fade_range:
                self.fade_fcurve.keyframe_points.insert(frame=point.x, value=point.y)
