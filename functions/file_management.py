"""Functions related to file management:
Fetching, loading and saving files to the disk."""
import bpy


def is_proxy(filename):
    """Checks if the file is a proxy generated with FFMPEG"""
    # TODO: Check the containing folder
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
        if is_type(file, file_type) and not is_proxy(file):
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


def create_text_file(name):
    """Create a new text file, name it and return it
        Args:
        -name, the name of the text file, a string"""
    if not name and isinstance(name, str):
        raise TypeError('The name of the text file has to be a string')

    bpy.ops.text.new()
    import re
    re_text = re.compile(r'^Text.[0-9]{3}$')

    text_name = ''
    text_index, max_index = 0, 0
    for text in bpy.data.texts:
        if re_text.match(text.name):
            text_index = int(text.name[-3:])
            if text_index > max_index:
                max_index = text_index
                text_name = text.name
    if not text_name:
        text_name = 'Text'

    bpy.data.texts[text_name].name = name
    return bpy.data.texts[name]