import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_marker_delete_direct(bpy.types.Operator):
    """
    Delete selected markers instantly skipping the default confirmation prompt
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.scene.timeline_markers) > 0

    def execute(self, context):
        markers = context.scene.timeline_markers

        selected_markers = [m for m in markers if m.select]
        for m in selected_markers:
            markers.remove(m)
        self.report({'INFO'}, "Deleted %s markers." % len(selected_markers))
        return {'FINISHED'}

