import os
import bpy


class ProjectSettings():
    RESOLUTION_X = 1920
    RESOLUTION_Y = 1080
    pass


class Extensions():
    """Tuples of file types for checks when importing files"""
    PSD = ("*.psd")
    IMG = ("*.png", "*.jpg", "*.jpeg")
    AUDIO = ("*.wav", "*.mp3", "*.ogg")
    VIDEO = ("*.mp4", "*.avi", "*.mts")


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


# FIXME: Currently not getting image width and height (set to 0)
def add_transform_effect(sequences=None):
    """Takes a list of image strips and adds a transform effect to them.
       Ensures that the pivot will be centered on the image"""
    sequencer = bpy.ops.sequencer
    sequence_editor = bpy.context.scene.sequence_editor
    render = bpy.context.scene.render

    sequences = [s for s in sequences if s.type in ('IMAGE', 'MOVIE')]

    if not sequences:
        return None

    sequencer.select_all(action='DESELECT')

    for s in sequences:
        s.mute = True

        sequence_editor.active_strip = s
        sequencer.effect_strip_add(type='TRANSFORM')

        active = sequence_editor.active_strip
        active.name = "TRANSFORM-%s" % s.name
        active.blend_type = 'ALPHA_OVER'
        active.select = False

    print("Successfully processed " + str(len(sequences)) +
          " image sequences")
    return True


# def calc_transform_effect_scale(sequence):
#     """Takes a transform effect and returns the scale it should use
#        to preserve the scale of its cropped input"""
#     # if not (sequence or sequence.type == 'TRANSFORM'):
#     #     raise AttributeError

#     s = sequence.input_1

#     crop_x, crop_y = s.elements[0].orig_width - (s.crop.min_x + s.crop.max_x),
#                      s.elements[0].orig_height - (s.crop.min_y + s.crop.max_y)
#     ratio_x, ratio_y = crop_x / render.resolution_x,
#                        crop_y / render.resolution_y
#     if ratio_x > 1 or ratio_y > 1:
#         ratio_x /= ratio_y
#         ratio_y /= ratio_x
#     return ratio_x, ratio_y
#     active.scale_start_x, active.scale_start_y = ratio_x ratio_y


def is_revolver_proxy(filename):
    """Checks if the file is a proxy generated with FFMPEG"""
    return True if '_proxy.' in filename else False


def is_type(filename=None, file_type=None):
    """Checks if a file is of a certain type that can be loaded by Blender (image, audio, video...)
    Input: filename (including the file extensions), and the file_type to check (pass an entry from the Extensions class)
    Returns True if the file extension is in the file type.

    Example uses:
    is_type("folder\\subfolder\\footage.mp4", Extensions.VIDEO) returns True
    is_type("video.mp4", Extensions.AUDIO) returns False """

    file_extension = filename[filename.rfind(".") + 1:].upper()
    # print(filename + " / " + file_extension)
    # print(file_type.value)

    if file_extension in file_type:
        return True
    else:
        return False


def get_working_directory(path=None):
    if not path:
        return False

    project_name = bpy.path.basename(path)
    directory = path[:len(path) - (len(project_name) + 1)]
    return directory


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

    if filetype == Extensions.IMG:
        sequencer.image_strip_add(sequencer_area, directory=directory, files=files,
                                  frame_start=start, frame_end=end, channel=channel)
    elif filetype == Extensions.VIDEO:
        sequencer.movie_strip_add(sequencer_area, filepath=directory,
                                  files=files, frame_start=start, channel=channel, sound=keep_audio)
    elif filetype == Extensions.AUDIO:
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
        elif file_type in [Extensions.VIDEO, Extensions.IMG]:
            subfolder = os.path.join(path, file)
            if os.path.isdir(subfolder):
                subfolders.append(subfolder)

    for folder in subfolders:
        for file in os.listdir(path=folder):
            if is_type(file, file_type):
                files.append({'name': os.path.split(
                    folder)[1] + "/" + file})

    return files, subfolders


# TODO: Refactor, walk directories and collect filepaths, then send to function
#       to create strips
# TODO: By default, do not reimport existing strips, import only the new ones
# TODO: Use add-on preferences to change default image length
# TODO: add option to add fade in and/or out by default to pictures
# TODO: add option to add default animation (ease in/out on X axis) on
class ImportLocalFootage2(bpy.types.Operator):
    bl_idname = "gdquest_vse.import_local_footage_2"
    bl_label = "Import local footage 2"
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
        created_img_strips = []


        FOLDER_NAMES = ('audio', 'img', 'video')
        working_directory = get_working_directory(path)
        folders = {}

        for d in os.listdir(path=working_directory):
            if d in FOLDER_NAMES:
                folders[d] = working_directory + "\\" + d

        def find_files(directory, file_extensions, recursive=False):
            """Walks through a folder and returns files matching the extensions.
               Then, converts the files to a list of dictionaries to import in Blender"""
            if not directory and file_extensions:
                return None

            from glob import glob
            files = []

            # TODO: Ignore "_proxy" folders
            # FIXME: glob doesn't return anything
            for ext in file_extensions:
                pattern = directory + "\\"
                pattern += "**." + ext if recursive else ext
                print(pattern)
                files.extend(glob(pattern))

            # TODO: Properly handle images
            # Psd assets folder
            # And img sequence
            files_dict = []
            for f in files:
                files_dict.extend({'name': f[len(directory):]})

            return {'path': directory, 'files': files_dict}

        # To add files, need a list of dictionaries like
        # {'name': 'path'} where path is relative to filepath
        audio_files = find_files(folders['audio'], Extensions.AUDIO)
        video_files = find_files(folders['video'], Extensions.VIDEO, recursive=True)
        img_files = find_files(folders['img'], Extensions.IMG, recursive=True)

        print(audio_files)
        print(video_files)
        print(img_files)



        # PROCESSING IMAGE STRIPS
        # sequencer.select_all(action='DESELECT')
        if created_img_strips:
            add_transform_effect(created_img_strips)
            for s in created_img_strips:
                s.select = True

        return {"FINISHED"}