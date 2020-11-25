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

    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def execute(self, context):
        
        max_channel = 32
        min_channel = 1

        def is_in_limit_channel(sequence):
            if self.direction == "up" and sequence.channel == max_channel:
                return True
            elif self.direction == "down" and sequence.channel == min_channel:
                return True
            else:
                return False
        
        def out_of_range():
            if target_end <= moving_start or moving_end <= target_start:   # <<<<<<<<<<<<
                return True
            else:
                return False

        selection = [s for s in context.selected_sequences if (
            not s.lock and not (self.direction == "down" and s.channel == min_channel)
            and not (self.direction == "up" and s.channel == max_channel)
        )]
        if not selection:
            return {"FINISHED"}
        
        # Sorts the "selection" list depending of the key press.
        # By default will be set to move downwards. If the direction is up, the list is reversed.
        selection = sorted(selection, key=attrgetter("channel", "frame_final_start"))
        if self.direction == "up":
            selection = reversed(selection)

        # Saves all selected strips to reselect them after the operation.
        rescue_selected = context.selected_sequences

        for moving_strip in selection:

            if self.trim_target_channel:

                to_delete = []
                strips_in_target_channel = []
                target_channel = (
                    min(max_channel, moving_strip.channel + 1) if self.direction == "up" 
                    else max(min_channel, moving_strip.channel - 1)
                )
                
                # Makes it easier to read.
                moving_start = moving_strip.frame_final_start
                moving_end = moving_strip.frame_final_end

                # s is any strip able to move.
                for target_strip in context.sequences:
                    
                    target_start = target_strip.frame_final_start
                    target_end = target_strip.frame_final_end
                    
                    # Checks if the moving strip could interact with the target strip.
                    if target_strip.channel == target_channel and not out_of_range():
                        bpy.ops.sequencer.select_all(action="DESELECT")

                        ###########################################################################
                        # Delete:
                        
                        # Makes a list with all strips that will be deleted if they are completely
                        # inside the range of the moving strip.
                        if moving_start <= target_start and target_end <= moving_end:
                            to_delete.append(target_strip)
                            continue

                        ###########################################################################
                        # Trim: 

                        # If the target strip's start/end are inside moving strip's range: divide
                        # in 3, delete the middle and select the last if the target was selected.
                        if target_start < moving_start and moving_end < target_end:
                            
                            target_strip.select = True
                            bpy.ops.sequencer.split(frame=moving_start, type="SOFT", side="RIGHT")
                            bpy.ops.sequencer.split(frame=moving_end, type="SOFT", side="LEFT")
                            to_delete.append(context.selected_sequences[0])

                            # Sets all strips in the target channel in a tuple.
                            # It's to correctly reselect the remaining bits of the trimmed strip.
                            for s in context.sequences:
                                if s.channel == target_channel:
                                    strips_in_target_channel.append(s)

                            # Appends the last trimmed strip to the rescue list
                            if target_strip in rescue_selected:
                                rescue_selected.append(strips_in_target_channel[0])
                            continue

                        # If the target strip's end is outside moving strip's range, trim target
                        # strip's start.
                        elif moving_start <= target_start:
                            
                            target_strip.frame_final_start = moving_strip.frame_final_end

                        # If the target strip's start is outside moving strip's range, trim target
                        # strip's end.
                        elif target_end <= moving_end:
                            
                            target_strip.frame_final_end = moving_strip.frame_final_start

                        ###########################################################################

                # Deletes all strips in "to_delete" by selecting them.
                bpy.ops.sequencer.select_all(action="DESELECT")
                for s in to_delete:
                    s.select = True
                bpy.ops.sequencer.delete()
                
                # Reselects all the initial strips.
                for s in rescue_selected:
                    s.select = True

            if self.direction == "up":
                moving_strip.channel = min(max_channel, moving_strip.channel + 1)
            elif self.direction == "down":
                moving_strip.channel = max(min_channel, moving_strip.channel - 1)
        return {"FINISHED"}
