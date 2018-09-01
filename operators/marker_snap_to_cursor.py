import bpy


class MarkerSnapToCursor(bpy.types.Operator):
    bl_idname = 'power_sequencer.marker_snap_to_cursor'
    bl_label = 'Snap Marker To Cursor'
    bl_description = 'Snap selected marker to the time cursor'
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
