"""Simple operations like save, delete, open the project directory..."""
import bpy
from bpy.props import EnumProperty
from .functions.sequences import get_frame_range, set_preview_range

class OpenProjectDirectory(bpy.types.Operator):
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
        path = get_working_directory()

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


class OpenPicturesFile(bpy.types.Operator):
    bl_idname = 'gdquest_vse.open_local_psd'
    bl_label = 'Open local psd'
    bl_description = 'Open a psd or kra file stored in the local img folder'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        import os
        folder_path = bpy.path.abspath("//img")
        for file in os.listdir(folder_path):
            if file.lower().endswith(('.psd', '.kra')):
                import sys
                import subprocess
                file_path = folder_path + "/" + file
                if sys.platform.startswith('darwin'):
                    subprocess.call(('open', file_path))
                elif os.name == 'nt':
                    os.startfile(file_path)
                elif os.name == 'posix':
                    subprocess.call(('xdg-open', file_path))
        return {'FINISHED'}


class DeleteDirect(bpy.types.Operator):
    """Deletes without prompting for confirmation"""
    bl_idname = "gdquest_vse.delete_direct"
    bl_label = "Delete Direct"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = bpy.context.selected_sequences
        bpy.ops.sequencer.delete()

        selection_length = len(selection)
        report_message = 'Deleted ' + str(selection_length) + ' sequence'
        report_message += 's' if selection_length > 1 else ''
        self.report({'INFO'}, report_message)
        return {"FINISHED"}


class SaveDirect(bpy.types.Operator):
    """Saves current file without prompting for confirmation"""
    bl_idname = "gdquest_vse.save_direct"
    bl_label = "Save Direct"
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


class CycleScenes(bpy.types.Operator):
    """Cycle through scenes"""
    bl_idname = "gdquest_vse.cycle_scenes"
    bl_label = "Cycle scenes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scenes = bpy.data.scenes
        screen = bpy.context.screen

        scene_count = len(scenes)
        for index in range(scene_count):
            if bpy.context.scene == scenes[index]:
                bpy.context.screen.scene = scenes[(index + 1) % scene_count]
                break
        return {'FINISHED'}


class TogglePreviewSelectedStrips(bpy.types.Operator):
    """Sets the preview range based on selected sequences"""
    bl_idname = "gdquest_vse.toggle_preview_selection"
    bl_label = "Toggle preview selection"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if bpy.context.scene.frame_start == 1:
            selection = bpy.context.selected_sequences
            if not selection:
                return {'CANCELLED'}
            frame_start, frame_end = get_frame_range(sequences=bpy.context.selected_sequences, get_from_start=False)
        else:
            frame_start, frame_end = get_frame_range(get_from_start=True)

        set_preview_range(frame_start, frame_end)
        return {'FINISHED'}


class SetTimeline(bpy.types.Operator):
    """Set the timeline start and end frame using the time cursor"""
    bl_idname = "gdquest_vse.set_timeline"
    bl_label = "Set timeline start and end"
    bl_options = {'REGISTER', 'UNDO'}

    adjust = EnumProperty(items=[
        ('start', 'start', 'start'),
        ('end', 'end', 'end')],
        name='Adjust',
        description='Change the start or the end frame of the timeline',
        default='start')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = bpy.context.scene
        if self.adjust == 'start':
            scene.frame_start = scene.frame_current
        elif self.adjust == 'end':
            scene.frame_end = scene.frame_current - 1
        return {'FINISHED'}
