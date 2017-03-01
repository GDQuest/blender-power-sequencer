"""Functions related to file management:
Fetching, loading and saving files to the disk."""
import bpy


def is_proxy(filename):
    """Checks if the file is a proxy generated with FFMPEG"""
    # TODO: Check the containing folder
    return True if '_proxy.' in filename else False


def is_type(filename=None, file_type=None):
    """
    Checks if a file is of a certain type that can be loaded by Blender (image, audio, video...)
    Input: filename (including the file extensions), and the file_type to check (pass an entry from the Extensions class)
    Returns True if the file extension is in the file type, else false

    Example uses:
    is_type("folder\\subfolder\\footage.mp4", Extensions.DICT["VIDEO"]) returns True
    is_type("video.mp4", Extensions.DICT["AUDIO"]) returns False
    """
    file_extension = filename[filename.rfind(".") + 1:].upper()
    response = True if file_extension in file_type else False
    return response


def get_working_directory():
    """
    Takes the path to the current .blend file and
    returns the project's root directory (where the .blend file is saved)
    """
    full_path = bpy.data.filepath
    project_name = bpy.path.basename(full_path)
    working_directory = full_path[:len(full_path) - (len(project_name) + 1)]
    return working_directory


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
        elif file_type in [Extensions.DICT["VIDEO"], Extensions.DICT["IMG"]]:
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