import bpy


class MetaSeparateAndTrim(bpy.types.Operator):
    bl_idname = "power_sequencer.meta_separate"
    bl_label = "UnMeta and Trim"
    bl_description = "UnMeta all selected meta strips and trim their content"
    bl_options = {'REGISTER', 'UNDO'}

    trim_content = bpy.props.BoolProperty(
        name="Trim Content",
        description="Trim the content of the Meta Strips to their extents",
        default=True)

    @classmethod
    def poll(cls, context):
        try:
            next(s for s in context.selected_sequences if s.type == 'META')
            return True
        except StopIteration:
            return False

    def execute(self, context):
        meta_strips = [s for s in context.selected_sequences if s.type == 'META']
        if self.trim_content:
            bpy.ops.power_sequencer.meta_trim_content_to_bounds()
        self.separate(meta_strips)
        return {'FINISHED'}

    def separate(self, meta_strips):
        bpy.ops.sequencer.select_all(action='DESELECT')
        for m in meta_strips:
            bpy.context.scene.sequence_editor.active_strip = m
            bpy.ops.sequencer.meta_separate()
