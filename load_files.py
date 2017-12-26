import os
import bpy
from bpy.props import BoolProperty, IntProperty

from .functions.global_settings import ProjectSettings, Extensions
from .functions.file_management import *
from .functions.sequences import find_empty_channel


# TODO: Fix img imported from subfolder -
class ImportLocalFootage(bpy.types.Operator):
    bl_idname = "power_sequencer.import_local_footage"
    bl_label = "PS.Import local footage"
    bl_description = "Import video and audio from the project \
                      folder to VSE strips"
    bl_options = {'REGISTER', 'UNDO'}

    import_all = BoolProperty(
        name="Always Reimport",
        description="If true, always import all local files to new strips. \
                    If False, only import new files (check if footage has \
                    already been imported to the VSE).",
        default=False)
    keep_audio = BoolProperty(
        name="Keep audio from video files",
        description="If False, the audio that comes with video files \
                     will not be imported",
        default=True)

    img_length = IntProperty(
        name="Image strip length",
        description="Controls the duration of the imported image strip",
        default=96,
        min=1)
    img_padding = IntProperty(
        name="Image strip padding",
        description="Padding added between imported image strips in frames",
        default=24,
        min=1)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report(
                {"ERROR_INVALID_INPUT"},
                "You need to save your project first. Import cancelled.")
            return {"CANCELLED"}

        sequencer = bpy.ops.sequencer
        context = bpy.context
        frame_current = bpy.context.scene.frame_current
        empty_channel = find_empty_channel()

        bpy.ops.screen.animation_cancel(restore_frame=True)

        # Store reference to the Sequencer area to import files to
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if not area.type == 'SEQUENCE_EDITOR':
                    continue
                SEQUENCER_AREA = {'window': window, 'screen': window.screen, 'area': area, 'scene': bpy.context.scene}

        # Find folders for audio, img and video strips
        FILE_TYPES = ("AUDIO", "IMG", "VIDEO")
        project_directory = get_working_directory()

        def find_folders_to_import(parent_directory):
            folders = {}
            for folder in os.listdir(path=parent_directory):
                folder_upper = folder.upper()
                if folder_upper in FILE_TYPES:
                    folders[folder_upper] = os.path.join(parent_directory, folder)
            return folders


        folders = find_folders_to_import(project_directory)
        files = {}
        for file_type in FILE_TYPES:
            if file_type not in folders.keys():
                continue
            files[file_type] = find_files(folders[file_type],
                                       Extensions.DICT[file_type],
                                       recursive=file_type == "IMG")

        # Find or create new text files to keep track of imported material
        TEXT_FILE_PREFIX = 'IMPORT_'
        import_files = {}
        for file_type in FILE_TYPES:
            if bpy.data.texts.get(TEXT_FILE_PREFIX + file_type):
                import_files[file_type] = bpy.data.texts[TEXT_FILE_PREFIX + file_type]

        if not import_files:
            for name in FILE_TYPES:
                import_files[name] = create_text_file(TEXT_FILE_PREFIX + name)
            assert len(import_files) == 3

        # Write new imported paths to the text files and import new strips
        channel_offset = 0
        new_sequences, new_video_sequences = [], []
        for name in FILE_TYPES:
            if name not in folders.keys():
                continue

            text_file_content = [line.body for line in bpy.data.texts[TEXT_FILE_PREFIX + name].lines]
            new_paths = [path for path in files[name] if path not in text_file_content]
            for line in new_paths:
                bpy.data.texts[TEXT_FILE_PREFIX + name].write(line + "\n")

            if not new_paths:
                continue

            # Import new strips if new files were found
            import_channel = empty_channel + channel_offset
            folder = folders[name]
            import_dict = files_to_dict(new_paths, folder)

            if name == "VIDEO":
                import_channel += 1 if self.keep_audio else 0
                project_root, _ = os.path.split(folder)
                import_frame = frame_current
                for d in import_dict:
                    sequencer.movie_strip_add(SEQUENCER_AREA,
                                            filepath=os.path.join(folder, d['name']),
                                            frame_start=import_frame,
                                            channel=import_channel,
                                            sound=self.keep_audio)
                    new_sequences.extend(bpy.context.selected_sequences)
                    new_video_sequences.extend(bpy.context.selected_sequences)
                    import_frame = bpy.context.selected_sequences[0].frame_final_end

                    audio_strip = None
                    video_strip = None
                    for s in bpy.context.selected_sequences:
                        if s.type == 'SOUND':
                            audio_strip = s
                        elif s.type == 'MOVIE':
                            video_strip = s

                    if not audio_strip:
                        continue
                    if abs(audio_strip.frame_final_end - video_strip.frame_final_end) == 1:
                        audio_strip.frame_final_end = video_strip.frame_final_end

            if name == "AUDIO":
                sequencer.sound_strip_add(
                    SEQUENCER_AREA,
                    filepath=folder,
                    files=import_dict,
                    frame_start=frame_current,
                    channel=import_channel)
                new_sequences.extend(bpy.context.selected_sequences)
            elif name == "IMG":
                img_frame = frame_current
                for img in import_dict:
                    path = os.path.join(folder, img['subfolder'])
                    # FIXME: temp hack so images import properly
                    file = [{'name': img['name'].replace("img\\", "")}]
                    sequencer.image_strip_add(
                        SEQUENCER_AREA,
                        directory=path,
                        files=file,
                        frame_start=img_frame,
                        frame_end=img_frame + self.img_length,
                        channel=import_channel)
                    new_sequences.extend(bpy.context.selected_sequences)
                    img_frame += self.img_length + self.img_padding
            channel_offset += 1

        if not new_video_sequences:
            return {"FINISHED"}

        # Swap channels for audio and video tracks
        sequencer.select_all(action='DESELECT')
        for s in new_video_sequences:
            s.select = True
        sequencer.meta_make()
        sequencer.meta_toggle()
        videos_in_meta = [s for s in bpy.context.selected_sequences if s.type == 'MOVIE']
        for s in videos_in_meta:
            s.channel += 2
        for s in new_video_sequences:
            s.channel -= 1
        sequencer.meta_toggle()
        sequencer.meta_separate()

        # Set the strips to use proxies based if set in the addon preferences
        # prefs = context.user_preferences.addons[__package__].preferences
        # if prefs.auto_render_proxies:
        #     bpy.ops.power_sequencer.set_video_proxies()

        # Show audio waveforms
        for s in [strip for strip in new_sequences if strip.type == 'SOUND']:
            s.show_waveform = True

        for s in new_sequences:
            s.select = True
        return {"FINISHED"}


# TODO: Ignore the blender proxy folders
# TODO: Detect img sequences
def find_files(directory,
               file_extensions,
               recursive=False,
               ignore_folders=('_proxy', 'BL_proxy')):
    """
    Walks through a folder and returns a list of filepaths
    that match the extensions.
    Args:
        - file_extensions is a tuple of extensions with the form "*.ext".
        Use the Extensions helper class in .functions.global_settings.
        It gives default extensions to check the files against.
    Returns a list of file paths, or [] if nothing was found
    """
    if not directory and file_extensions:
        return None

    files = []

    from glob import glob
    from os.path import basename

    # TODO: Folder containing img files = img sequence?
    # Or rather: if files' heads end with 001, 002, 003...
    for ext in file_extensions:
        source_pattern = directory + "/"
        pattern = source_pattern + ext
        files.extend(glob(pattern))
        if not recursive:
            continue
        pattern = source_pattern + "**/" + ext
        files.extend(glob(pattern))

    if basename(directory) == "IMG":
        psd_names = [f for f in glob(directory + "/*.psd")]
        for i, name in enumerate(psd_names):
            psd_names[i] = name[len(directory):-4]

        psd_folders = (f for f in os.listdir(directory) if f in psd_names)
        for f in psd_folders:
            for ext in file_extensions:
                files.extend(glob(directory + "/" + f + "/" + ext))
    return files


# TODO: issue with img vs other strip types: img have separate filepath and filename slots
# but video/audio only have direct filepath e.g. audio/file.wav
def files_to_dict(files, folder_path):
    """Converts a list of files to Blender's dictionary format for import
       Returns a list of dictionaries with the
       {'name': filename, 'subfolder': subfolder} format
       If the provided files are placed at the root of the import folders,
       subfolder will be an empty string
       Args:
        - files: a list or a tuple of files
        - folder_path: a string of the path to the files' containing folder"""
    if not files and folder_path:
        return None

    dictionary = []
    for f in files:
        filepath_tail = f[len(folder_path) + 1:]
        head, tail = os.path.split(filepath_tail)

        project_path, subfolder_name = os.path.split(folder_path)
        dict_form = {'name': tail, 'subfolder': head}
        dictionary.append(dict_form)
    return dictionary
