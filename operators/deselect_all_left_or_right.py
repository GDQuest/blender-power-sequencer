import bpy
import operator

class DeselectAllStripsLeftOrRight(bpy.types.Operator):
    """
    Deselects all the strips at the left or right of the time cursor, based
    on the position of the mouse.
    """
    bl_idname = "power_sequencer.deselect_all_left_or_right"
    bl_label = "Deselect Strips to Left or Right"
    bl_description = """Deselects all the strips to the left or right of the
                        time cursor, based on the position of the mouse."""
    bl_options = {'REGISTER', 'UNDO'}

    side = bpy.props.EnumProperty(
		name="Side",
		description="The side to deselect",
		items=[
			("mouse", "Mouse position", "Deselect based on the mouse position relative to the time cursor"),
			("left", "Left", "Left of the time cursor"),
			("right", "Right", "Right of the time cursor")
		],
        default="mouse"
	)
    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_sequences) > 0

    def invoke(self, context, event):
        frame_current = context.scene.frame_current
        frame_mouse = context.region.view2d.region_to_view(event.mouse_region_x, 1)[0]

        for s in bpy.context.sequences:
            if frame_mouse < frame_current or self.side == "left":
                if s.frame_final_end < frame_current:
                    self.deselect(s)
            elif frame_mouse >= frame_current or self.side == "right":
                if s.frame_final_start >= frame_current:
                    self.deselect(s)
        return {'FINISHED'}

    def deselect(self, strip):
        strip.select = False
        strip.select_left_handle = False
        strip.select_right_handle = False
