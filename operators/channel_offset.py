#
# Copyright (C) 2016-2020 by Nathan Lovato, Daniel Oakey, Razvan Radulescu, and contributors
#
# This file is part of Power Sequencer.
#
# Power Sequencer is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Power Sequencer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Power Sequencer. If
# not, see <https://www.gnu.org/licenses/>.
#
import bpy
from operator import attrgetter

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description
from .utils.functions import (
    slice_selection,
    trim_strips,
    find_strips_in_range,
    move_selection,
    pixel_frame_ratio,
)


class POWER_SEQUENCER_OT_channel_offset(bpy.types.Operator):
    """
    Move selected strip to the nearest open channel above/down
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "",
        "description": doc_description(__doc__),
        "shortcuts": [
            (
                {"type": "UP_ARROW", "value": "PRESS", "alt": True},
                {"direction": "up", "trim_target_channel": False},
                "Move to Open Channel Above",
            ),
            (
                {"type": "UP_ARROW", "value": "PRESS", "ctrl": True, "alt": True},
                {"direction": "up", "trim_target_channel": True},
                "Move to Channel Above and Trim",
            ),
            (
                {"type": "DOWN_ARROW", "value": "PRESS", "alt": True},
                {"direction": "down", "trim_target_channel": False},
                "Move to Open Channel Below",
            ),
            (
                {"type": "DOWN_ARROW", "value": "PRESS", "ctrl": True, "alt": True},
                {"direction": "down", "trim_target_channel": True},
                "Move to Channel Below and Trim",
            ),
        ],
        "keymap": "Sequencer",
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc["name"]
    bl_description = doc_brief(doc["description"])
    bl_options = {"REGISTER", "UNDO"}

    direction: bpy.props.EnumProperty(
        items=[
            ("up", "up", "Move the selection 1 channel up"),
            ("down", "down", "Move the selection 1 channel down"),
        ],
        name="Direction",
        description="Move the sequences up or down",
        default="up",
    )
    trim_target_channel: bpy.props.BoolProperty(
        name="Trim strips",
        description="Trim strips to make space in the target channel",
        default=False,
    )
    keep_selection_offset: bpy.props.BoolProperty(
        name="Keep selection offset",
        description="The selected strips preserve their relative positions",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def execute(self, context):
        
        max_channel = 32
        min_channel = 1

        if self.direction == "up":
            movement = + 1
            limit_channel = max_channel
            movement_to_limit = min

        if self.direction == "down":
            movement = - 1
            limit_channel = min_channel
            movement_to_limit = max


        selection = [s for s in context.selected_sequences if not s.lock]

        if not selection:
            return {"FINISHED"}
        
        range_block = round(47 * pixel_frame_ratio(context, "x"))
        '''
        If keep_selection_offset, sets all the strips by blocks. The blocks consists of strips
        close enough between each other. The minimum distance is range_block, which uses the real
        distance from the screen (pixel/frame) and not just frames. That means more strips will
        in the same block the larger the view is, and viceversa.
        Parts:
            - Arbitrary number which is convinient for the functionality. Bigger means more apart.
            - pixel_frame_ratio("x") gives the current relation frame/pixel on screen of the sequencer panel in
            the given axis.
        '''

        selection_blocks = slice_selection(context, selection, range_block)
        for block in selection_blocks:
            sequences = sorted(block, key=attrgetter("channel", "frame_final_start"))
            if self.direction == "up":
                sequences = [s for s in reversed(sequences)]

            head = sequences[0]
            if self.keep_selection_offset == False or (not head.channel == limit_channel and self.keep_selection_offset == True):

                if self.trim_target_channel:
                    to_remove = []
                    for s in sequences:
                        if s.channel == limit_channel:
                            to_remove.append(s)
                            continue

                        channel_trim = movement_to_limit(limit_channel, s.channel + movement)
                        all_strips = [c for c in context.sequences if c.channel == channel_trim]
                        if all_strips:
                            to_delete, to_trim = find_strips_in_range(s.frame_final_start, s.frame_final_end, all_strips)
                            trim_strips(context, s.frame_final_start, s.frame_final_end, to_trim, to_delete)
                        s.channel = movement_to_limit(limit_channel, s.channel + movement)
                        to_remove.append(s)
                    for s in to_remove:
                        sequences.remove(s)
                
                # Movement of strips
                if sequences:
                    start_frame = head.frame_final_start
                    x_difference = 0

                    if self.keep_selection_offset:
                        while not head.channel == limit_channel:
                            move_selection(context, sequences, -x_difference, movement)
                            x_difference = head.frame_final_start - start_frame
                            if x_difference == 0:
                                break
                    else:
                        for s in sequences: 
                            '''
                            There is an internal bug when going to pass the 32nd channel.
                            The side_movement to not overlap is always to the right,
                            whether it's close to the left edge of the upper strip or not.
                            Solves an internal bug of overlapping at max_channel when jumping 2+
                            strips.
                            '''
                            s.channel = movement_to_limit(limit_channel, s.channel + movement)
                            if s.channel == limit_channel:
                                move_selection(context, [s], 0, 0)

        return {"FINISHED"}
