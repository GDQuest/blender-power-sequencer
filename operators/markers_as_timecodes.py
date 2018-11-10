import bpy
import operator
import math
from .utils import pyperclip

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class CopyMarkersAsTimecodes(bpy.types.Operator):
    """
    Formats and copies all the markers as timecodes to put in a Youtube video's description
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        render = context.scene.render

        if len(context.scene.timeline_markers) == 0:
            self.report({'INFO'}, "No markers found")
            return {'CANCELLED'}

        sorted_markers = sorted(context.scene.timeline_markers,
                                key=operator.attrgetter('frame'))

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

