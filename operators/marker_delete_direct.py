import bpy


class MarkerDeleteDirect(bpy.types.Operator):
    """
    Delete selected markers instantly, skipping the default confirmation prompt
    """
    bl_idname = 'power_sequencer.marker_delete_direct'
    bl_label = 'Delete Markers Instantly'
    bl_description = 'Delete selected markers without asking for confirmation'
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
