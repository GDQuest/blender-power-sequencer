import bpy
from operator import attrgetter

from .utils.global_settings import SequenceTypes
from .utils.find_sequences_after import find_sequences_after
from .utils.find_strips_mouse import find_strips_mouse
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel


class ConcatenateStrips(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/YyEL8YP.gif)

    Concatenates selected strips in a channel (removes the gap between
    them) If a single strip is selected, either the next strip in the
    channel will be concatenated, or all strips in the channel will be
    concatenated depending on which shortcut is used.
    """
    bl_idname = "power_sequencer.concatenate_strips"
    bl_label = "Concatenate Strips"
    bl_description = "Remove space between strips"
    bl_options = {'REGISTER', 'UNDO'}

    concatenate_whole_channel = bpy.props.BoolProperty(
        name="Concatenate all strips in channel",
        description="If only one strip selected, concatenate the entire channel",
        default=False)
    frame, channel = -1, -1

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        self.frame, self.channel = get_mouse_frame_and_channel(event)
        return self.execute(context)

    def execute(self, context):
        sequences = context.selected_sequences if context.selected_sequences else find_strips_mouse(self.frame, self.channel, select_linked=False)
        # Only one sequence selected per channel
        channels = set([s.channel for s in sequences])
        if len(channels) == len(sequences):
            for s in sequences:
                in_channel = [strip for strip in find_sequences_after(s) if strip.channel == s.channel]
                in_channel.append(s)
                to_concatenate = [strip for strip in in_channel if strip.type in SequenceTypes.CONCATENATE]
                self.concatenate(to_concatenate)
        else:
            channels = list(set([s.channel for s in sequences]))
            for channel in channels:
                self.concatenate([s for s in sequences if s.channel == channel])
        return {"FINISHED"}

    def concatenate(self, sequences):
        """
        Takes a list of sequences in a single channel, sorts them by frame_final_start,
        and concatenates them.
        """
        if len(sequences) <= 1:
            return
        sorted_sequences = sorted(sequences, key=attrgetter('frame_final_start'))
        first_strip = sorted_sequences[0]
        if self.concatenate_whole_channel or len(sorted_sequences) > 2:
            to_concatenate = sorted_sequences[1:]
        else:
            first_strip.select = False
            second_strip = sorted_sequences[1]
            second_strip.select = True
            to_concatenate = [second_strip]

        concatenate_start = first_strip.frame_final_end
        for s in to_concatenate:
            gap = s.frame_final_start - concatenate_start
            s.frame_start -= gap
            concatenate_start += s.frame_final_duration
