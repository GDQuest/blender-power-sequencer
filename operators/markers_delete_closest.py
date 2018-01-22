import bpy
from .utils.find_neighboring_markers import find_neighboring_markers


class DeleteClosestMarker(bpy.types.Operator):
    bl_idname = 'power_sequencer.delete_closest_marker'
    bl_label = 'PS.Delete closest marker'
    bl_description = 'Delete the marker closest to the mouse'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        markers = bpy.context.scene.timeline_markers
        if not markers:
            return {"CANCELLED"}

        frame = bpy.context.scene.frame_current
        for m in markers:
            if m.frame == frame:
                markers.remove(m)
                return {'FINISHED'}

        previous_marker, next_marker = find_neighboring_markers(frame)

        marker = next_marker if next_marker else previous_marker
        if next_marker and previous_marker:
            if abs(frame - next_marker.frame) <= abs(frame -
                                                     previous_marker.frame):
                marker = next_marker
            else:
                marker = previous_marker
        markers.remove(marker)
        return {'FINISHED'}
