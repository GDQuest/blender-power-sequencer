import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class MarkerSnapToCursor(bpy.types.Operator):
    """
    Snap selected marker to the time cursor
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
        return True

    def execute(self, context):
        markers = bpy.context.scene.timeline_markers

        selected_markers = []
        for marker in markers:
            if marker.select:
                selected_markers.append(marker)

        if not selected_markers:
            return {'CANCELLED'}
        if len(selected_markers) > 1:
            self.report(
                {"ERROR_INVALID_INPUT"},
                "You can only snap 1 marker at a time. Operation cancelled.")
            return {'CANCELLED'}

        selected_markers[0].frame = bpy.context.scene.frame_current
        return {'FINISHED'}

