#
# Copyright (C) 2016-2019 by Nathan Lovato, Daniel Oakey, Razvan Radulescu, and contributors
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


class POWER_SEQUENCER_OT_add_transform(bpy.types.Operator):
    """
    *brief* Add transform effect to selected image and movie strips, centering and scaling images.


    For each selected sequence:

    - Centers the pivot point of image strips, and scales them down to their original size
    - Adds a transform effect and sets it to the alpha over blending mode
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "",
        "description": doc_description(__doc__),
        "shortcuts": [({"type": "T", "alt": True, "value": "PRESS"}, {}, "Add Transform")],
        "keymap": "Sequencer",
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc["name"]
    bl_description = doc_brief(doc["description"])
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        sequence_editor = context.scene.sequence_editor
        render = context.scene.render

        sequences = [s for s in context.selected_sequences if s.type in ("IMAGE", "MOVIE")]
        if not sequences:
            self.report({"ERROR_INVALID_INPUT"}, "No sequences movie or image strips selected")
            return {"FINISHED"}

        # Center image strips pivot
        for s in [s for s in sequences if s.type == "IMAGE"]:
            if s.use_translation and (s.transform.offset_x != 0 or s.transform.offset_y != 0):
                continue

            image_width = s.elements[0].orig_width
            image_height = s.elements[0].orig_height
            if image_width == 0 or image_height == 0:
                raise ValueError("image_height or image_width is 0")

            if image_width < render.resolution_x or image_height < render.resolution_y:
                s.use_translation = True
                s.transform.offset_x = (render.resolution_x - image_width) / 2
                s.transform.offset_y = (render.resolution_y - image_height) / 2

        sequencer.select_all(action="DESELECT")
        transform_strips = []
        for s in sequences:
            s.select = True
            sequence_editor.active_strip = s
            sequencer.effect_strip_add(type="TRANSFORM")

            transform = sequence_editor.active_strip
            transform.name = "TRANSFORM-{!s}".format(s.name)
            transform.blend_type = "ALPHA_OVER"
            transform_strips.append(transform)
            transform.select = False
            s.mute = True
            s.select = False

        for s in transform_strips + sequences:
            s.select = True
        sequence_editor.active_strip = transform_strips[0]
        return {"FINISHED"}
