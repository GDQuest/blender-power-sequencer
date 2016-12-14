import os
from enum import Enum

import bpy


def find_empty_channel(mode='ABOVE'):
    """Finds and returns the first empty channel in the VSE
    Takes the optional argument mode: 'ABOVE' or 'ANY'
    'ABOVE' finds the first empty channel above all of the other strips
    'ANY' finds the first empty channel, even if there are strips above it"""

    sequences = bpy.context.sequences

    if not sequences:
        return 1

    empty_channel = None
    channels = [s.channel for s in sequences]
    # remove duplicates and sort channels
    channels = sorted(list(set(channels)))

    for i in range(channels[-1]):
        if i not in channels:
            if mode == 'ANY':
                empty_channel = i
                break
    if not empty_channel:
        empty_channel = channels[-1] + 1

    return empty_channel


# TODO: Move parameters to PropertyGroup and preferences
# TODO: add option to add fade in and/or out
# TODO: add option to add default animation (ease in/out on X axis) on

# TODO: Refactor to scale transform from the center
def setup_image_strips(sequences=None):
    """Takes a list of image strips and adds a transform effect to them"""
    sequencer = bpy.ops.sequencer
    sequence_editor = bpy.context.scene.sequence_editor

    if not sequences:
        return None

    sequencer.select_all(action='DESELECT')

    for s in sequences:
        if s.type == 'IMAGE':
            sequence_editor.active_strip = s
            sequencer.effect_strip_add(type='TRANSFORM')
            # The transform strip automatically becomes active and selected
            sequence_editor.active_strip.blend_type = 'ALPHA_OVER'
            sequence_editor.active_strip.select = False
        else:
            print("The strip " + s.name + " is not an image strip")

    print("Successfully processed " + str(len(sequences)) +
          " image sequences")
    return True


def is_revolver_proxy(filename):
    """Checks if the file is a proxy generated with FFMPEG"""
    return True if '_proxy.' in filename else False


class FileTypes(Enum):
    """"""
    psd = "PSD"
    img = ("PNG", "JPG", "JPEG")
    audio = ("WAV", "MP3", "OGG")
    video = ("MP4", "AVI", "MTS")


def is_type(filename=None, file_type=None):
    """Checks if a file is of a certain type that can be loaded by Blender (image, audio, video...)
    Input: filename (including the file extensions), and the file_type to check (pass an entry from the FileTypes Enum)
    Returns True if the file extension is in the file type.

    Example uses:
    is_type("folder\\subfolder\\footage.mp4", FileTypes.video) returns True
    is_type("video.mp4", FileTypes.audio) returns False """

    file_extension = filename[filename.rfind(".") + 1:].upper()
    # print(filename + " / " + file_extension)
    # print(file_type.value)

    if file_extension in file_type.value:
        return True
    else:
        return False


def get_working_directory(path=None):
    if not path:
        return False

    project_name = bpy.path.basename(path)
    directory = path[:len(path) - (len(project_name) + 1)]
    return directory


# TODO: By default, do not reimport existing strips, import only the new ones and refresh the sequencer - But option to always import all
# TODO: After import, callback sync_audio_and_video.
#       If video and audio files have the same name, remove audio channel from video and sync remaining audio and video strips (if there's audio channel with video)
# TODO: Use add-on preferences to change default image length
class ImportLocalFootage(bpy.types.Operator):
    bl_idname = "gdquest_vse.import_local_footage"
    bl_label = "Import local footage"
    bl_description = "Import video and audio from the project folder to VSE strips"
    bl_options = {'REGISTER', 'UNDO'}

    always_import = bpy.props.BoolProperty(
        name="Always Reimport",
        description="If true, always import all local files to new strips. \
                    If False, only import new files (check if footage has \
                    already been imported to the VSE).",
        default=False)
    keep_audio = bpy.props.BoolProperty(
        name="Keep audio from video files",
        description="If False, the audio that comes with video files will not be imported",
        default=False)
    img_length = bpy.props.IntProperty(
        name="Image strip length",
        description="Controls the duration of the imported image strips length",
        default=96,
        min=1)
    img_padding = bpy.props.IntProperty(
        name="Image strip padding",
        description="Padding added between imported image strips in frames",
        default=24,
        min=1)
    # PSD related features
    import_psd = bpy.props.BoolProperty(
        name="Import PSD as image",
        description="When True, psd files will be imported as individual image strips",
        default=False)
    ps_assets_as_img = bpy.props.BoolProperty(
        name="Import PS assets as images",
        description="Imports the content of folders generated by Photoshop's quick export \
                    function as individual image strips",
        default=True)

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        if not bpy.data.is_saved:
            return {"CANCELLED"}

        sequencer = bpy.ops.sequencer
        context = bpy.context
        path = bpy.data.filepath

        bpy.ops.screen.animation_cancel(restore_frame=True)

        # TODO: remove after refactor
        wm = bpy.context.window_manager
        sequencer_area = {'region': wm.windows[0].screen.areas[2].regions[0],
                          'blend_data': bpy.context.blend_data,
                          'scene': bpy.context.scene,
                          'window': wm.windows[0],
                          'screen': bpy.data.screens['Video Editing'],
                          'area': bpy.data.screens['Video Editing'].areas[2]}

        # TODO: REIMPORT
        # check_strip_names = False
        channel_for_audio = 1 if self.keep_audio else 0
        empty_channel = find_empty_channel(mode='ABOVE')
        directory = get_working_directory(path)

        # TODO: REFACTOR AND USE FUNCTIONS
        for entry in os.listdir(path=directory):
            strip_insert_frame = 1

            if entry == 'video':
                # video_files = get_files_from_folder(directory, entry)
                video_path = directory + '\\' + entry
                folder_content = os.listdir(path=video_path)

                if not folder_content:
                    continue

                video_channel = empty_channel + 1
                videos, subfolders = [], []

                for video in folder_content:
                    if is_type(video, FileTypes.video) and not is_revolver_proxy(video):
                        videos.append({'name': video})
                    else:
                        subfolder = os.path.join(video_path, video)
                        if os.path.isdir(subfolder):
                            subfolders.append(subfolder)

                for folder in subfolders:
                    for video in os.listdir(path=folder):
                        if is_type(video, FileTypes.video):
                            videos.append({'name': os.path.split(
                                folder)[1] + "/" + video})

                sequencer.movie_strip_add(sequencer_area, filepath=video_path + "\\" + video,
                                          files=videos, frame_start=1, channel=video_channel, sound=self.keep_audio)
            elif entry == 'audio':
                audio_folder_content = os.listdir(path=(directory + '\\' + entry))

                if not audio_folder_content:
                    continue

                audio_channel = empty_channel
                audio_path = directory + '\\' + entry

                for audio in audio_folder_content:
                    if is_type(audio, FileTypes.audio):
                        sequencer.sound_strip_add(
                            sequencer_area, filepath=audio_path + "\\" + audio, frame_start=strip_insert_frame, channel=audio_channel)
                        strip_insert_frame += context.sequences[0].frame_final_duration
            elif entry == 'img':
                img_folder_content = os.listdir(
                    path=directory + '\\' + entry)

                if not img_folder_content:
                    continue

                image_channel = empty_channel + 2 + channel_for_audio
                image_path = directory + '\\' + entry

                for image in img_folder_content:
                    is_image = is_type(image, FileTypes.img) if not self.import_psd \
                        else is_type(image, FileTypes.img) or is_type(image, FileTypes.psd)

                    if is_image:
                        sequencer.image_strip_add(
                            sequencer_area,
                            directory=image_path,
                            files=[{'name': image}],
                            frame_start=strip_insert_frame,
                            frame_end=strip_insert_frame + self.img_length,
                            channel=image_channel)
                        strip_insert_frame += self.img_length + self.img_padding + 1
                    # IMAGE SEQUENCE and ASSETS FOLDER
                    else:
                        subfolder = os.path.join(image_path, image)
                        if os.path.isdir(subfolder):
                            subfolder_files = os.listdir(path=subfolder)
                            if len(subfolder_files) > 0:
                                is_ps_assets_folder = True if subfolder[
                                    len(subfolder) -
                                    7:] == '-assets' and self.ps_assets_as_img else False

                                image_files = []
                                for item in subfolder_files:
                                    if is_type(item, FileTypes.img):
                                        if is_ps_assets_folder:
                                            sequencer.image_strip_add(
                                                sequencer_area,
                                                directory=subfolder,
                                                files=[{'name': item}],
                                                frame_start=strip_insert_frame,
                                                frame_end=strip_insert_frame +
                                                self.img_length,
                                                channel=image_channel)
                                            strip_insert_frame += self.img_length + self.img_padding + 1
                                        else:
                                            image_files.append({'name': item})
                                if len(image_files) > 0:
                                    sequencer.image_strip_add(
                                        sequencer_area,
                                        directory=subfolder,
                                        files=image_files,
                                        frame_start=strip_insert_frame,
                                        frame_end=strip_insert_frame + len(image_files),
                                        channel=image_channel)
                                    strip_insert_frame += self.img_length + self.img_padding + 1
        # PROCESSING IMAGE STRIPS
        image_strips = []
        for s in context.sequences:
            if s.type == 'IMAGE':
                image_strips.append(s)
        setup_image_strips(image_strips)

        sequencer.select_all(action='DESELECT')

        return {"FINISHED"}


def add_strip_from_file(filetype, directory, files, start, end, channel, keep_audio=False):
    """Add a file or a list of files as a strip to the VSE"""
    sequencer = bpy.ops.sequencer
    wm = bpy.context.window_manager
    sequencer_area = {'region': wm.windows[0].screen.areas[2].regions[0],
                      'blend_data': bpy.context.blend_data,
                      'scene': bpy.context.scene,
                      'window': wm.windows[0],
                      'screen': bpy.data.screens['Video Editing'],
                      'area': bpy.data.screens['Video Editing'].areas[2]}

    if filetype == FileTypes.img:
        sequencer.image_strip_add(sequencer_area, directory=directory, files=files,
                                  frame_start=start, frame_end=end, channel=channel)
    elif filetype == FileTypes.video:
        sequencer.movie_strip_add(sequencer_area, filepath=directory,
                                  files=files, frame_start=start, channel=channel, sound=keep_audio)
    elif filetype == FileTypes.audio:
        sequencer.sound_strip_add(
            sequencer_area, filepath=directory, frame_start=start, channel=channel)

    return "SUCCESS"


def get_files_from_folder(path, folder_name, file_type):
    """Returns a dictionary of files to add as strips to the VSE"""
    if not path and folder_name and file_type:
        return []

    files, subfolders = [], []
    path += '\\' + folder_name
    folder_content = os.listdir(path=path)

    if not folder_content:
        return []

    for file in folder_content:
        if is_type(file, file_type) and not is_revolver_proxy(file):
            files.append({'name': file})
        elif file_type in [FileTypes.video, FileTypes.img]:
            subfolder = os.path.join(path, file)
            if os.path.isdir(subfolder):
                subfolders.append(subfolder)

    for folder in subfolders:
        for file in os.listdir(path=folder):
            if is_type(file, file_type):
                files.append({'name': os.path.split(
                    folder)[1] + "/" + file})

    return files, subfolders
