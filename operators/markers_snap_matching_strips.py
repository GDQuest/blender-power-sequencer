import bpy


class MarkersSnapMatchingStrips(bpy.types.Operator):
    """
    Snap selected strips to markers with the same name
    """
    bl_idname = 'power_sequencer.markers_snap_matching_strips'
    bl_label = 'Markers Snap Matching Strips'
    bl_description = 'Snap selected strips to markers with the same name'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.scene.timeline_markers) > 0

    def execute(self, context):
        timeline_markers = context.scene.timeline_markers

        for strip in context.selected_sequences:
            for marker in timeline_markers:
                if marker.name in strip.name:
                    strip.frame_start = marker.frame - strip.frame_offset_start
        return {'FINISHED'}
