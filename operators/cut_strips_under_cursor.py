import bpy


class CutStripsUnderCursor(bpy.types.Operator):
    bl_idname = 'power_sequencer.cut_strips_under_cursor'
    bl_label = 'Cut strips under cursor'
    bl_description = ('Cuts all strips under cursor (without needing '
                      'selection first), including mutted strips. It '
                      'excludes locked strips.')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0

    def execute(self, context):
        (context.selected_sequences
         or bpy.ops.power_sequencer.select_strips_under_cursor())
        return bpy.ops.sequencer.cut(frame=context.scene.frame_current)

