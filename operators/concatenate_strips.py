import bpy
from operator import attrgetter

from .utils.global_settings import SequenceTypes
from .utils.find_next_sequences import find_next_sequences
from .utils.filter_sequences_by_type import filter_sequences_by_type


class ConcatenateStrips(bpy.types.Operator):
    """
    Concatenates selected strips (removes space between them)
    If a single strip is selected, finds all the strips after it in the channel
    """
    bl_idname = "power_sequencer.concatenate_strips"
    bl_label = "PS.Concatenate strips"
    bl_options = {'REGISTER', 'UNDO'}

    concatenate_whole_channel = bpy.props.BoolProperty(
        name="Concatenate all strips in channel",
        description="If only one strip selected, concatenate the entire channel",
        default=False)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        def concatenate_sequences(sequences):
            """
            Takes a list of sequences and concatenates them
            Mutates the sequences directly, doesn't return anything
            """
            for channel in channels:
                concat_sequences = [
                    s for s in sequences if s.channel == channel
                ]
                concat_start = concat_sequences[0].frame_final_end
                concat_sequences.pop(0)

                for s in concat_sequences:
                    gap = s.frame_final_start - concat_start
                    s.frame_start -= gap
                    concat_start += s.frame_final_duration
            return

        sequences = bpy.context.selected_sequences

        # If only 1 sequence selected, find next sequences in channel
        first_strip = None
        if len(sequences) == 1:
            first_strip = sequences[0]
            in_channel = [
                s for s in find_next_sequences(sequences)
                if s.channel == first_strip.channel
            ]

            for s in in_channel:
                sequences.append(s)

        sequences = filter_sequences_by_type(sequences, SequenceTypes.VIDEO,
                                             SequenceTypes.IMAGE,
                                             SequenceTypes.SOUND)
        if len(sequences) <= 1:
            self.report({"INFO"}, "No strips to concatenate.")
            return {'CANCELLED'}

        channels = list(set([s.channel for s in sequences]))
        sequences = sorted(
            sequences, key=attrgetter('channel', 'frame_final_start'))

        if not self.concatenate_whole_channel and first_strip:
            next_strip = sequences[1]
            concatenate_sequences([first_strip, next_strip])

            first_strip.select = False
            next_strip.select = True
            return {"FINISHED"}

        concatenate_sequences(sequences)
        return {"FINISHED"}
