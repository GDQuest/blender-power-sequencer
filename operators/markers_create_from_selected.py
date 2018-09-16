import bpy


class MarkersCreateFromSelectedStrips(bpy.types.Operator):
    bl_idname = "power_sequencer.markers_create_from_selected"
    bl_label = "Markers from Selected Strips"
    bl_description = "Create one marker at the start on each selected strip, \
            based on its name. Use it to copy markers as timecodes."

    @classmethod
    def poll(cls, context):
        return len(context.selected_sequences) > 0

    def execute(self, context):
        cursor_frame_start = bpy.context.scene.frame_current

        for m in context.scene.timeline_markers:
            m.select = False

        for s in context.selected_sequences:
            bpy.ops.marker.add()
            new_marker = bpy.context.scene.timeline_markers[-1]

            new_marker.select = True
            bpy.ops.marker.rename(name=s.name)
            gap = s.frame_final_start - cursor_frame_start
            bpy.ops.marker.move(frames=gap)
            new_marker.select = False
        return {'FINISHED'}
