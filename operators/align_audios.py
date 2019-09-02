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


class POWER_SEQUENCER_OT_align_audios(bpy.types.Operator):
    """
    *brief* Align two similar audios


    Attempt alignment between the selected audio strip to the active
    audio strip. The better the correlation, the better the result.

    This operator requires
    [ffmpeg](https://www.ffmpeg.org/download.html) and
    [scipy](https://www.scipy.org/install.html) to work. Audio must be
    converted to WAV data prior to analyzing, so longer strips may take
    longer to align. To mitigate this issue, analysis will be limited to
    the first 15 minutes of audio at most.
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "https://i.imgur.com/xkBUzDj.gif",
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
        scene = context.scene
        if scene.sequence_editor and scene.sequence_editor.active_strip:
            active = scene.sequence_editor.active_strip
            selected = context.selected_sequences

            if len(selected) == 2 and active in selected:
                selected.pop(selected.index(active))
                if selected[0].type == "SOUND" and active.type == "SOUND":
                    return context.selected_sequences
        return False

    def execute(self, context):
        try:
            import scipy
        except ImportError:
            self.report({"ERROR"}, "Scipy must be installed to align audios")
            return {"FINISHED"}

        if not is_ffmpeg_available():
            self.report({"ERROR"}, "ffmpeg must be installed to align audios")
            return {"FINISHED"}

        # This import is here because it slows blender startup a little
        from .audiosync import find_offset

        scene = context.scene

        active = scene.sequence_editor.active_strip
        active_filepath = bpy.path.abspath(active.sound.filepath)

        selected = context.selected_sequences
        selected.pop(selected.index(active))

        align_strip = selected[0]
        align_strip_filepath = bpy.path.abspath(align_strip.sound.filepath)

        offset, score = find_offset(align_strip_filepath, active_filepath)

        initial_offset = active.frame_start - align_strip.frame_start

        fps = scene.render.fps / scene.render.fps_base
        frames = int(offset * fps)

        align_strip.frame_start -= frames - initial_offset

        self.report({"INFO"}, "Alignment score: " + str(round(score, 1)))

        return {"FINISHED"}


def is_ffmpeg_available():
    """
    Returns true if ffmpeg is installed and available from the PATH
    """
    try:
        subprocess.call(["ffmpeg", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except OSError:
        return False
