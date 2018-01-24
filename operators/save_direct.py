import bpy


class SaveDirect(bpy.types.Operator):
    """Saves current file without prompting for confirmation"""
    bl_idname = "power_sequencer.save_direct"
    bl_label = "Save direct"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if bpy.data.is_saved:
            bpy.ops.wm.save_mainfile()
        else:
            bpy.ops.wm.save_as_mainfile({'dict': "override"}, 'INVOKE_DEFAULT')
        self.report({'INFO'}, 'File saved')
        return {"FINISHED"}
