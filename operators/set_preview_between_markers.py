import bpy
from .utils.find_neighboring_markers import find_neighboring_markers


class SetPreviewBetweenMarkers(bpy.types.Operator):
    bl_idname = 'power_sequencer.set_preview_between_markers'
    bl_label = 'Set preview between markers'
    bl_description = "Set the timeline's preview range using the 2 markers closest to the time cursor"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        if not bpy.context.scene.timeline_markers:
            self.report({"ERROR_INVALID_INPUT"},
                        "There are no markers. Operation cancelled.")
            return {"CANCELLED"}

        frame = bpy.context.scene.frame_current
        previous_marker, next_marker = find_neighboring_markers(frame)

        if not (previous_marker and next_marker):
            self.report({"ERROR_INVALID_INPUT"},
                        "There are no markers. Operation cancelled.")
            return {"CANCELLED"}

        frame_start = previous_marker.frame if previous_marker else 0
        if next_marker:
            frame_end = next_marker.frame
        else:
            from operator import attrgetter
            frame_end = max(
                bpy.context.scene.sequence_editor.sequences,
                key=attrgetter('frame_final_end')).frame_final_end

        from .utils.sequences import set_preview_range
        set_preview_range(frame_start, frame_end)
        return {'FINISHED'}
