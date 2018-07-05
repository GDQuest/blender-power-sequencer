import bpy
import operator
import math
from .utils import pyperclip


class CopyMarkersAsTimecodes(bpy.types.Operator):
    bl_idname = "power_sequencer.markers_as_timecode"
    bl_label = "Markers as Timecodes"
    bl_description = "Formats and copies all the markers as \
        timecodes to put in a Youtube video's description"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        render = context.scene.render

        if len(context.scene.timeline_markers) == 0:
            self.report({'INFO'}, "No markers found")
            return {'CANCELLED'}

        sorted_markers = sorted(context.scene.timeline_markers, key=operator.attrgetter('frame'))

        markers_as_timecodes = ""
        for marker in sorted_markers:
            framerate = render.fps / render.fps_base
            time_in_seconds = marker.frame / framerate
            minutes = math.floor(time_in_seconds / 60.0)
            seconds = math.floor(time_in_seconds % 60.0)

            string = "{:02d}:{:02d} {}".format(minutes, seconds, marker.name)
            markers_as_timecodes += string + "\n"

        pyperclip.copy(markers_as_timecodes)
        return {'FINISHED'}
