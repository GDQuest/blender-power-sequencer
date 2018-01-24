import bpy
from .utils.find_neighboring_markers import find_neighboring_markers


class GoToNextMarker(bpy.types.Operator):
    """Moves the time cursor to the next marker"""
    bl_idname = "power_sequencer.go_to_next_marker"
    bl_label = "Go to next marker"
    bl_options = {'REGISTER', 'UNDO'}

    target_marker = bpy.props.EnumProperty(
        items=[('left', 'left', 'left'), ('right', 'right', 'right')],
        name='Target marker',
        description='Move to the closest marker to the left or to the right of the cursor',
        default='left')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if not bpy.context.scene.timeline_markers:
            self.report({"ERROR_INVALID_INPUT"},
                        "There are no markers. Operation cancelled.")
            return {"CANCELLED"}

        frame = bpy.context.scene.frame_current
        previous_marker, next_marker = find_neighboring_markers(frame)

        if not previous_marker and self.target_marker == 'left' or not next_marker and self.target_marker == 'right':
            self.report({"INFO"}, "No more markers to jump to on the %s side."
                        % self.target_marker)
            return {"CANCELLED"}

        previous_time = previous_marker.frame if previous_marker else None
        next_time = next_marker.frame if next_marker else None

        bpy.context.scene.frame_current = previous_time if self.target_marker == 'left' or not next_time else next_time
        return {'FINISHED'}
