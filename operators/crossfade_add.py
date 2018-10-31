import bpy
from operator import attrgetter
from .utils.find_sequences_after import find_sequences_after
from .utils.convert_duration_to_frames import convert_duration_to_frames
from .utils.global_settings import SequenceTypes


# TODO: update docstrings
class CrossfadeAdd(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/ZyEd0jD.gif)

    For each selected strip, finds the next sequence in the channel,
    optionally moves it next to the first strip, and adds
    a gamma cross effect between them.
    Currently works with MOVIE, IMAGE and META strips.
    """
    bl_idname = "power_sequencer.crossfade_add"
    bl_label = "Add Crossfade"
    bl_description = ("Adds cross fade between selected sequence and the"
                      " closest sequence to its right")
    bl_options = {"REGISTER", "UNDO"}

    crossfade_duration = bpy.props.FloatProperty(
        name="Crossfade Duration",
        description="The duration of the crossfade",
        default=0.5,
        min=0)
    auto_move_strip = bpy.props.BoolProperty(
        name="Auto Move Strip",
        description=("When true, moves the second strip so the crossfade"
                     " is of the length set in 'Crossfade Length'"),
        default=True)

    @classmethod
    def poll(cls, context):
        try:
            next(s for s in context.sequences if s.type not in
                 SequenceTypes.TRANSITION + SequenceTypes.SOUND)
            return True
        except StopIteration:
            return False

    def execute(self, context):
        sorted_selection = sorted(context.selected_sequences,
                                  key=attrgetter('frame_final_start'))
        for selected_strip in sorted_selection:
            next_in_channel = [s for s in find_sequences_after(selected_strip)
                               if s.channel == selected_strip.channel]
            if not next_in_channel:
                continue
            next_transitionable = (s for s in next_in_channel
                                   if s.type in SequenceTypes.TRANSITIONABLE)
            next_sequence = min(next_transitionable,
                                key=attrgetter('frame_final_start'))

            if self.auto_move_strip:
                frame_offset = (next_sequence.frame_final_start -
                                selected_strip.frame_final_end)
                next_sequence.frame_start -= frame_offset

            if next_sequence.frame_final_start == \
               selected_strip.frame_final_end:
                crossfade_length = convert_duration_to_frames(
                    self.crossfade_duration
                )
                next_sequence.frame_final_start += crossfade_length / 2
                selected_strip.frame_final_end -= crossfade_length / 2

            self.apply_crossfade(selected_strip, next_sequence)
        return {"FINISHED"}

    def apply_crossfade(self, strip_from, strip_to):
        bpy.ops.sequencer.select_all(action='DESELECT')
        strip_from.select = True
        strip_to.select = True
        bpy.context.scene.sequence_editor.active_strip = strip_to
        bpy.ops.sequencer.effect_strip_add(type='GAMMA_CROSS')

