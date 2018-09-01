import bpy
from operator import attrgetter


class MarkerDeleteClosest(bpy.types.Operator):
    """
    Deletes the marker closest to the time cursor
    """
    bl_idname = "power_sequencer.marker_delete_closest"
    bl_label = "Delete Closest Marker"
    bl_description = "Delete the marker closest to the mouse"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.scene.timeline_markers) > 0

    def invoke(self, context, event):
        markers = context.scene.timeline_markers
        frame = context.scene.frame_current

        closest_marker = min(markers, key=lambda marker: abs(frame - marker.frame))
        markers.remove(closest_marker)
        return {'FINISHED'}
