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

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_value_offset(bpy.types.Operator):
    """
    Move the selection given frames or seconds to the left/right
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "",
        "description": doc_description(__doc__),
        "shortcuts": [
            (
                {"type": "LEFT_ARROW", "value": "PRESS", "shift": True, "alt": True},
                {"direction": "left"},
                "Move to Left Given Seconds",
            ),
            (
                {"type": "RIGHT_ARROW", "value": "PRESS", "shift": True, "alt": True},
                {"direction": "right"},
                "Move to Right Given Seconds",
            ),
        ],
        "keymap": "Sequencer",
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc["name"]
    bl_description = doc_brief(doc["description"])
    bl_options = {"REGISTER", "UNDO"}

    
    # Hidden as the user mustn't and doesn't have to touch it.
    direction: bpy.props.EnumProperty(
        items=[
            ("left", "left", "Move the selection to the left"),
            ("right", "right", "Move the selection to the right"),
            ("none", "none", "Direction which the operations are made")
        ],
        name="Direction",
        description="Move the selection given frames or seconds",
        default="right",
        options={'HIDDEN'},
    )

    value_type: bpy.props.EnumProperty(
        items=[
            ("seconds", "Seconds", "Move with the value as seconds"),
            ("frames", "Frames", "Move with the value as frames"),
        ],
        name="Value Type",
        description="Set the value type to be operated",
        default="seconds",
    )

    value_offset: bpy.props.FloatProperty(
        name="Value",
        description="Move the selection the number of frames or seconds",
        default=1.0,
        step=5,
        precision=3,
        subtype='NONE',
    )

    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def execute(self, context):

        if self.direction == "left":
            self.value_offset = - abs(self.value_offset)

        if self.direction == "right":
            self.value_offset = abs(self.value_offset)
        
        # Used to reset the direction
        self.direction = "none"

        if self.value_type == "seconds":
            
            fps = bpy.context.scene.render.fps
            fps_base = bpy.context.scene.render.fps_base
            fps_rate = fps / fps_base
            frames_offset = self.value_offset * fps_rate
        else:
            frames_offset = round(self.value_offset)
            self.value_offset = frames_offset

        bpy.ops.transform.seq_slide(value=(frames_offset, 0))

        return {"FINISHED"}
