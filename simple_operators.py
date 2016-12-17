import bpy
from bpy.types import Operator

class OpenProjectDirectory(Operator):
    bl_idname = 'gdquest_vse.open_project_directory'
    bl_label = 'Open project directory'
    bl_description = 'Opens the Blender project directory in the explorer'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        from subprocess import Popen
        from platform import system

        from .load_files import get_working_directory

        path = get_working_directory(path=bpy.data.filepath)

        if not path:
            self.report({'WARNING'}, "You have to save your project first.")
            return {'CANCELLED'}

        if system() == "Windows":
            Popen(["explorer", path])
        elif system() == "Darwin":
            Popen(["open", path])
        else:
            Popen(["xdg-open", path])
        return {'FINISHED'}


class DeleteDirect(bpy.types.Operator):
    """Deletes without prompting for confirmation"""
    bl_idname = "gdquest_vse.delete_direct"
    bl_label = "Delete Direct"
    bl_options = {'REGISTER', 'UNDO'}
    # Shortcut: Delete

    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

    def execute(self, context):
        selection = bpy.context.selected_sequences
        bpy.ops.sequencer.delete()

        selection_length = len(selection)
        report_message = 'Deleted ' + str(selection_length) + ' sequence'
        report_message += 's' if selection_length > 1 else ''
        self.report({'INFO'}, report_message)
        return {"FINISHED"}


# TODO: If file not saved, fire up save as
class SaveDirect(bpy.types.Operator):
    """Saves current file without prompting for confirmation"""
    bl_idname = "gdquest_vse.save_direct"
    bl_label = "Save Direct"
    bl_options = {'REGISTER', 'UNDO'}
    # Shortcut: Ctrl + S

    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

    def execute(self, context):
        if bpy.data.is_saved:
            bpy.ops.wm.save_mainfile()
        else:
            bpy.ops.wm.save_as_mainfile({'dict': "override"}, 'INVOKE_DEFAULT')
        self.report({'INFO'}, 'File saved')
        return {"FINISHED"}
