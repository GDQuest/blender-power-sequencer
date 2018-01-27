import bpy


class BorderSelect(bpy.types.Operator):
    bl_idname = 'power_sequencer.border_select'
    bl_label = 'Border Select'
    bl_description = "Wrapper around Blender's border select, deselects handles"

    bl_options = {'REGISTER', 'UNDO'}

    extend = bpy.props.BoolProperty(
        name="Extend the selection",
        description="Extend the current selection if checked, otherwise clear it",
        default=False)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for s in bpy.context.selected_sequences:
            s.select_right_handle = False
            s.select_left_handle = False
        bpy.ops.sequencer.select_border('INVOKE_DEFAULT', extend=self.extend)
        return {'FINISHED'}
