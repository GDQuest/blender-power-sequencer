import bpy
import os
from platform import system
from subprocess import Popen


class OpenProjectDirectory(bpy.types.Operator):
    bl_idname = 'power_sequencer.open_project_directory'
    bl_label = 'PS.Open project directory'
    bl_description = 'Opens the Blender project directory in the explorer'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        path = os.path.split(bpy.data.filepath)[0]

        if not path:
            self.report({'INFO'}, "You have to save your project first.")
            return {'CANCELLED'}

        if system() == "Windows":
            Popen(["explorer", path])
        elif system() == "Darwin":
            Popen(["open", path])
        else:
            Popen(["xdg-open", path])
        return {'FINISHED'}
