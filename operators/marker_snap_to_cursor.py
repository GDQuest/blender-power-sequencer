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


class POWER_SEQUENCER_OT_marker_snap_to_cursor(bpy.types.Operator):
    """
    Snap selected marker to the time cursor
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "",
        "description": doc_description(__doc__),
        "shortcuts": [],
        "keymap": "Sequencer",
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc["name"]
    bl_description = doc_brief(doc["description"])
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.scene.timeline_markers

    def execute(self, context):
        markers = context.scene.timeline_markers

        selected_markers = []
        for marker in markers:
            if marker.select:
                selected_markers.append(marker)

        if not selected_markers:
            return {"CANCELLED"}
        if len(selected_markers) > 1:
            self.report(
                {"ERROR_INVALID_INPUT"},
                "You can only snap 1 marker at a time. Operation cancelled.",
            )
            return {"CANCELLED"}

        selected_markers[0].frame = context.scene.frame_current
        return {"FINISHED"}
