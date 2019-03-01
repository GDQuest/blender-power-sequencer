import bpy
from operator import attrgetter

from .utils.find_sequences_after import find_sequences_after
from .utils.convert_duration_to_frames import convert_duration_to_frames
from .utils.global_settings import SequenceTypes
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_crossfade_add(bpy.types.Operator):
    """
    *brief* Adds cross fade between selected sequence and the closest sequence to its right


    Based on the active strip, finds the closest next sequence of a similar type, moves it
    so it overlaps the active strip, and adds a gamma cross effect between them. Works with
    MOVIE, IMAGE and META strips
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': 'https://i.imgur.com/ZyEd0jD.gif',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'C', 'value': 'PRESS', 'ctrl': True, 'alt': True}, {}, 'Add Crossfade')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {"REGISTER", "UNDO"}

    crossfade_duration: bpy.props.FloatProperty(
        name="Crossfade Duration",
        description="The duration of the crossfade",
        default=0.5,
        min=0)
    auto_move_strip: bpy.props.BoolProperty(
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
        except (StopIteration, TypeError):
            return False

    def execute(self, context):
        sorted_selection = sorted(context.selected_sequences,
                                  key=attrgetter('frame_final_start'))
        # Try to add a crossfade for each selected strip
        for selected_strip in sorted_selection:
            next_in_channel = [s for s in find_sequences_after(context, selected_strip)
                               if s.channel == selected_strip.channel]
            if not next_in_channel:
                continue
            next_transitionable = (s for s in next_in_channel
                                   if s.type in SequenceTypes.TRANSITIONABLE)
            try:
                next_sequence = min(next_transitionable,
                                    key=attrgetter('frame_final_start'))
            except ValueError:
                continue

            if self.auto_move_strip:
                frame_offset = (next_sequence.frame_final_start -
                                selected_strip.frame_final_end)
                next_sequence.frame_start -= frame_offset

            if next_sequence.frame_final_start == \
               selected_strip.frame_final_end:
                crossfade_length = convert_duration_to_frames(
                    context,
                    self.crossfade_duration
                )
                next_sequence.frame_final_start += crossfade_length / 2
                selected_strip.frame_final_end -= crossfade_length / 2

            self.apply_crossfade(context, selected_strip, next_sequence)
        return {"FINISHED"}

    def apply_crossfade(self, context, strip_from, strip_to):
        bpy.ops.sequencer.select_all(action='DESELECT')
        strip_from.select = True
        strip_to.select = True
        context.scene.sequence_editor.active_strip = strip_to
        bpy.ops.sequencer.effect_strip_add(type='GAMMA_CROSS')
