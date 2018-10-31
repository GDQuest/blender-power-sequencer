import bpy


class CutStripsUnderCursor(bpy.types.Operator):
    bl_idname = 'power_sequencer.cut_strips_under_cursor'
    bl_label = 'Cut strips under cursor'
    bl_description = ('Cuts all strips under cursor (without needing '
                      'selection first), including mutted strips. It '
                      'excludes locked strips.')
    bl_options = {'REGISTER', 'UNDO'}

    frame = bpy.props.IntProperty(name="Frame")
    channel = bpy.props.IntProperty(name="Channel")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.power_sequencer.select_strips_under_cursor()
        return bpy.ops.sequencer.cut(frame=context.scene.frame_current,
                                     type='SOFT')

