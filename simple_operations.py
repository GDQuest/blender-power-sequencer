"""Simple operations like save, delete, open the project directory..."""
import bpy
from bpy.props import EnumProperty, BoolProperty
from operator import attrgetter
import os
from subprocess import Popen
from platform import system
from .functions.sequences import get_frame_range, set_preview_range, \
    slice_selection


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


class OpenPicturesFile(bpy.types.Operator):
    bl_idname = 'power_sequencer.open_local_psd'
    bl_label = 'PS.Open local psd'
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
    bl_idname = "power_sequencer.delete_direct"
    bl_label = "PS.Delete Direct"
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


class CopySelectedSequences(bpy.types.Operator):
    """
    Copies the selected sequences without frame offset and optionally deletes the selection to give a cut to clipboard effect
    """
    bl_idname = "power_sequencer.copy_selection"
    bl_label = "PS.Copy or cut sequences"
    bl_options = {'REGISTER', 'UNDO'}

    delete_selection = BoolProperty(
        name="Delete selection",
        description="Delete selected strips: acts like cut and paste",
        default=False)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = bpy.context.selected_sequences
        cursor_start_frame = bpy.context.scene.frame_current
        sequencer = bpy.ops.sequencer

        # Deactivate audio playback
        scene = bpy.context.scene
        initial_audio_setting = scene.use_audio_scrub
        scene.use_audio_scrub = False

        first_sequence = min(selection, key=attrgetter('frame_final_start'))
        bpy.context.scene.frame_current = first_sequence.frame_final_start
        sequencer.copy()
        bpy.context.scene.frame_current = cursor_start_frame

        scene.use_audio_scrub = initial_audio_setting

        if self.delete_selection:
            sequencer.delete()

        plural_string = 's' if len(selection) != 1 else ''
        action_verb = 'Cut' if self.delete_selection else 'Copied'
        report_message = '{!s} {!s} sequence{!s} to the clipboard.'.format(
            action_verb, str(len(selection)), plural_string)
        self.report({'INFO'}, report_message)
        return {"FINISHED"}


class SaveDirect(bpy.types.Operator):
    """Saves current file without prompting for confirmation"""
    bl_idname = "power_sequencer.save_direct"
    bl_label = "PS.Save Direct"
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
    bl_idname = "power_sequencer.cycle_scenes"
    bl_label = "PS.Cycle scenes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scenes = bpy.data.scenes

        scene_count = len(scenes)

        if bpy.context.screen.is_animation_playing:
            bpy.ops.screen.animation_cancel(restore_frame=False)
        for index in range(scene_count):
            if bpy.context.scene == scenes[index]:
                bpy.context.screen.scene = scenes[(index + 1) % scene_count]
                break
        return {'FINISHED'}


class TogglePreviewSelectedStrips(bpy.types.Operator):
    """Sets the preview range based on selected sequences"""
    bl_idname = "power_sequencer.toggle_preview_selection"
    bl_label = "PS.Toggle preview selection"
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
            sequences=bpy.context.selected_sequences, get_from_start=False)

        if scene.frame_start == frame_start and scene.frame_end == frame_end:
            frame_start, frame_end = get_frame_range(get_from_start=True)

        set_preview_range(frame_start, frame_end)
        return {'FINISHED'}


class SetTimeline(bpy.types.Operator):
    """Set the timeline start and end frame using the time cursor"""
    bl_idname = "power_sequencer.set_timeline"
    bl_label = "PS.Set timeline start and end"
    bl_options = {'REGISTER', 'UNDO'}

    adjust = EnumProperty(
        items=[('start', 'start', 'start'), ('end', 'end', 'end')],
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


# TODO: To do a proper ripple, gotta move the sequences "manually" i.e. when you delete the
# first sequence on the leftmost side of the sequencer
# TODO: Improve auto move cursor back
class RippleDelete(bpy.types.Operator):
    bl_idname = 'power_sequencer.ripple_delete'
    bl_label = 'PS.Ripple delete'
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
        cursor_offset = 0

        channels = set((s.channel for s in selection))

        audio_scrub = bpy.context.scene.use_audio_scrub
        if audio_scrub:
            bpy.context.scene.use_audio_scrub = False

        # If only 1 block of strips, we store linked strips
        selection_blocks = slice_selection(selection)

        surrounding_strips = []
        is_single_channel = len(selection_blocks) == 1 and len(channels) == 1
        if is_single_channel:
            bpy.ops.sequencer.select_linked()
            for s in bpy.context.selected_sequences:
                if s not in selection:
                    surrounding_strips.append(s)
            sequencer.select_all(action='DESELECT')
            for s in selection_blocks[0]:
                s.select = True
            sequencer.delete()

        else:
            for block in selection_blocks:
                sequencer.select_all(action='DESELECT')
                for s in block:
                    s.select = True
                selection_start, _ = get_frame_range(block)
                sequencer.delete()

                scene.frame_current = selection_start
                sequencer.gap_remove(all=False)

            # auto move cursor back
            if bpy.context.screen.is_animation_playing and len(
                    selection_blocks) == 1:
                sequences = selection_blocks[0]
                start_frame = min(
                    sequences,
                    key=attrgetter('frame_final_start')).frame_final_start
                end_frame = max(
                    sequences,
                    key=attrgetter('frame_final_end')).frame_final_end
                delete_duration = end_frame - start_frame
                if scene.frame_current > start_frame:
                    cursor_offset = delete_duration

        # Concatenate
        if is_single_channel:
            for s in surrounding_strips:
                s.select = True
            bpy.ops.power_sequencer.concatenate_strips()

        scene.frame_current = cursor_start - cursor_offset
        report_message = 'Deleted ' + str(selection_length) + ' sequence'
        report_message += 's' if selection_length > 1 else ''
        self.report({'INFO'}, report_message)
        if audio_scrub:
            bpy.context.scene.use_audio_scrub = audio_scrub

        return {'FINISHED'}
