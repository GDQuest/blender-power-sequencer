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
            screen = window.screen
            for area in screen.areas:
                if area.type == 'SEQUENCE_EDITOR':
                    SEQUENCER_AREA = {'window': window,
                                      'screen': screen,
                                      'area': area,
                                      'scene': bpy.context.scene}


        # Find folders for audio, img and video strips
        directory = get_working_directory()
        folders, files, files_dict = {}, {}, {}
        file_types = "AUDIO", "IMG", "VIDEO"

        for folder in os.listdir(path=directory):
            folder_upper = folder.upper()
            if folder_upper in file_types:
                folders[folder_upper] = os.path.join(directory, folder)

        for file_type in file_types:
            if file_type not in folders.keys():
                continue
            files[file_type] = find_files(folders[file_type],
                                       Extensions.DICT[file_type],
                                       recursive=file_type == "IMG")

        # TODO: walk the project dir tree and collect all files that have a supported Extension
        #
        # files, files_dict = {}, {}
        # file_types = "AUDIO", "IMG", "VIDEO"
        # for file_type in file_types:
        #     files[file_type] = find_files_temp(get_working_directory(),
        #                                   Extensions.DICT[file_type])
        # filepaths = []
        # for dirpath, dirname, filenames in os.walk(directory, topdown=True):
        # for filename in filenames:
        #     files.append(os.path.join(dirparth, filename)

        # Find or create new text files to keep track of imported material
        TEXT_FILE_PREFIX = 'IMPORT_'
        texts = bpy.data.texts
        import_files = {}
        for file_type in file_types:
            if texts.get(TEXT_FILE_PREFIX + file_type):
                import_files[file_type] = texts[TEXT_FILE_PREFIX + file_type]

        if not import_files:
            for name in file_types:
                import_files[name] = create_text_file(TEXT_FILE_PREFIX + name)
            assert len(import_files) == 3

        # Write new imported paths to the text files and import new strips
        channel_offset = 0
        new_sequences, new_video_sequences = [], []
        for name in file_types:
            if name not in folders.keys():
                continue

            text_file_content = [
                line.body
                for line in bpy.data.texts[TEXT_FILE_PREFIX + name].lines
            ]
            new_paths = [path
                         for path in files[name]
                         if path not in text_file_content]
            for line in new_paths:
                bpy.data.texts[TEXT_FILE_PREFIX + name].write(line + "\n")

            if not new_paths:
                continue

            # Import new strips if new files were found
            import_channel = empty_channel + channel_offset
            folder = folders[name]
            files_dict = files_to_dict(new_paths, folder)

            if name == "VIDEO":
                import_channel += 1 if self.keep_audio else 0
                sequencer.movie_strip_add(SEQUENCER_AREA,
                                          filepath=folder,
                                          files=files_dict,
                                          frame_start=frame_current,
                                          channel=import_channel,
                                          sound=self.keep_audio)
                new_sequences.extend(bpy.context.selected_sequences)
                # Blender places audio tracks on top, we want them under video
                new_video_sequences.extend(bpy.context.selected_sequences)
            elif name == "AUDIO":
                sequencer.sound_strip_add(
                    SEQUENCER_AREA,
                    filepath=folder,
                    files=files_dict,
                    frame_start=frame_current,
                    channel=import_channel)
                new_sequences.extend(bpy.context.selected_sequences)
            elif name == "IMG":
                img_frame = frame_current
                for img in files_dict:
                    path = os.path.join(folder, img['subfolder'])
                    file = [{'name': img['name']}]
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

        # Swap channels for audio and video tracks
        if not new_video_sequences:
            return {"FINISHED"}

        # Reorder the sequences so all MOVIE strips are on top
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
        prefs = context.user_preferences.addons[__package__].preferences
        if prefs.auto_render_proxies:
            bpy.ops.power_sequencer.set_video_proxies()

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
        dict_form = {'name': os.path.join(subfolder_name, tail), 'subfolder': head}
        dictionary.append(dict_form)
    return dictionary
