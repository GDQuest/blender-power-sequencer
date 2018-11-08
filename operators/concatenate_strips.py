import bpy
from operator import attrgetter

from .utils.global_settings import SequenceTypes
from .utils.find_sequences_after import find_sequences_after
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel


def find_sequences_before(strip):
    """
    Returns a list of sequences that are before the strip in the current context
    """
    return [
        s for s in bpy.context.sequences
        if s.frame_final_end <= strip.frame_final_start
    ]


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

    concatenate_all = bpy.props.BoolProperty(
        name="Concatenate all strips in channel",
        description=
        "If only one strip selected, concatenate the entire channel",
        default=False)
    direction = bpy.props.EnumProperty(
        name="Direction",
        description=
        "Concatenate strips moving them back in time (default) or forward in time",
        items=[('left', "Left", "Move strips back in time, to the left"),
               ('right', "Right",
                "Move strips forward in time, to the right")],
        default='left')
    frame, channel = -1, -1

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        frame, channel = get_mouse_frame_and_channel(event)
        if not context.selected_sequences:
            bpy.ops.power_sequencer.select_closest_to_mouse(
                frame=frame, channel=channel)
        return self.execute(context)

    def execute(self, context):
        selection = context.selected_sequences
        one_strip_only = True if len(selection) == 1 else False
        channels = {s.channel for s in selection}

        # If only one strip selected per channel,
        # Loop over each strip and detect which strips to concatenate
        if len(channels) == len(selection):
            for s in selection:
                if self.direction == 'right':
                    in_channel = [strip for strip in find_sequences_before(s)
                                  if strip.channel == s.channel]
                else:
                    in_channel = [strip for strip in find_sequences_after(s)
                                  if strip.channel == s.channel]
                in_channel.append(s)
                to_concatenate = [strip for strip in in_channel
                                  if strip.type in SequenceTypes.CONCATENATE]

                if self.direction == 'right':
                    self.concatenate_right(to_concatenate, one_strip_only)
                else:
                    self.concatenate_left(to_concatenate, one_strip_only)
        else:
            for channel in channels:
                to_concatenate = [s for s in selection if s.channel == channel]
                if self.direction == 'right':
                    self.concatenate_right(to_concatenate)
                else:
                    self.concatenate_left(to_concatenate)
        return {'FINISHED'}

    def concatenate_left(self, sequences, one_strip_only=False):
        """
        Takes a list of sequences in a single channel, sorts them by frame_final_start,
        and concatenates them.
        """
        if len(sequences) <= 1:
            return
        sorted_sequences = sorted(
            sequences, key=attrgetter('frame_final_start'))
        first_strip = sorted_sequences[0]
        if self.concatenate_all or not one_strip_only:
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
            concatenate_start = s.frame_final_end

    def concatenate_right(self, sequences, one_strip_only=False):
        """
        Takes a list of sequences in a single channel, sorts them by frame_final_start,
        and concatenates them moving strips forward in time, towards the last strip in the
        ordered list
        """
        if len(sequences) <= 1:
            return
        sorted_sequences = sorted(sequences, key=attrgetter('frame_final_start'))
        last_strip = sorted_sequences.pop()
        if self.concatenate_all or not one_strip_only:
            to_concatenate = sorted_sequences
        else:
            last_strip.select = False
            second_strip = sorted_sequences.pop()
            second_strip.select = True
            to_concatenate = [second_strip]
        print(to_concatenate)

        concatenate_start = last_strip.frame_final_start
        print(concatenate_start)
        for s in reversed(to_concatenate):
            gap = s.frame_final_end - concatenate_start
            s.frame_start -= gap
            concatenate_start = s.frame_final_start
