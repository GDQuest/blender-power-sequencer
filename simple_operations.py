"""Simple operations like save, delete, open the project directory..."""
import bpy
from bpy.props import EnumProperty
from .functions.sequences import get_frame_range, set_preview_range, \
    slice_selection


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
        scene = bpy.context.scene
        selection = bpy.context.selected_sequences
        if not selection:
            return {'CANCELLED'}
        frame_start, frame_end = get_frame_range(
            sequences=bpy.context.selected_sequences,
            get_from_start=False)

        if scene.frame_start == frame_start and scene.frame_end == frame_end:
            frame_start, frame_end = get_frame_range(get_from_start=True)

        set_preview_range(frame_start, frame_end)
        return {'FINISHED'}


class SetTimeline(bpy.types.Operator):
    """Set the timeline start and end frame using the time cursor"""
    bl_idname = "gdquest_vse.set_timeline"
    bl_label = "Set timeline start and end"
    bl_options = {'REGISTER', 'UNDO'}

    adjust = EnumProperty(
        items=[
            ('start', 'start', 'start'), ('end', 'end', 'end')
        ],
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


# TODO: If deleting in a single channel, concatenate based on connected sequences?
class RippleDelete(bpy.types.Operator):
    bl_idname = 'gdquest_vse.ripple_delete'
    bl_label = 'Ripple delete'
    bl_description = 'Delete the selected sequences and remove gaps'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = bpy.context.scene
        sequencer = bpy.ops.sequencer
        selection = bpy.context.selected_sequences

        if not selection:
            return {'CANCELLED'}

        selection_length = len(selection)
        cursor_start = scene.frame_current
        channels = set((s.channel for s in selection))

        audio_scrub = bpy.context.scene.use_audio_scrub
        if audio_scrub:
            bpy.context.scene.use_audio_scrub = False

        # If only 1 block of strips, we store linked strips
        selection_blocks = slice_selection(selection)

        surrounding_strips = []
        is_single_block = len(selection_blocks) == 1 and len(channels) == 1
        if is_single_block:
            bpy.ops.sequencer.select_linked()
            for s in bpy.context.selected_sequences:
                if s not in selection:
                    surrounding_strips.append(s)

        for block in selection_blocks:
            sequencer.select_all(action='DESELECT')
            for s in block:
                s.select = True
            selection_start, _ = get_frame_range(block)
            scene.frame_current = selection_start + 1
            sequencer.delete()
            sequencer.gap_remove(all=False)

        # If single block, concatenate (useful for audio)
        if is_single_block:
            for s in surrounding_strips:
                s.select = True
            bpy.ops.gdquest_vse.concatenate_strips()

        scene.frame_current = cursor_start
        report_message = 'Deleted ' + str(selection_length) + ' sequence'
        report_message += 's' if selection_length > 1 else ''
        self.report({'INFO'}, report_message)
        if audio_scrub:
            bpy.context.scene.use_audio_scrub = audio_scrub
        return {'FINISHED'}
