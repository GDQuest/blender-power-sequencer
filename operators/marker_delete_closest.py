import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class MarkerDeleteClosest(bpy.types.Operator):
    """
    Deletes the marker closest to the time cursor
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
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.scene.timeline_markers) > 0

    def invoke(self, context, event):
        markers = context.scene.timeline_markers
        frame = context.scene.frame_current

        closest_marker = min(markers,
                             key=lambda marker: abs(frame - marker.frame))
        markers.remove(closest_marker)
        return {'FINISHED'}

