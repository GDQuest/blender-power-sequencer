import argparse
import os
import subprocess
import sys

def get_working_directory(path):
    """
    If path is an actually directory its absolute path is returned. If it is a
    .blend file the absolute path to the containing directory is returned. In
    all other cases an exception is raised.
    """
    abs_path = os.path.abspath(path)
    if os.path.exists(abs_path):
        if os.path.isdir(abs_path):
            return abs_path
        elif os.path.isfile(abs_path) and abs_path.endswith(".blend"):
            return os.path.dirname(abs_path)
    raise ValueError("{} is neither a directory nor a .blend file".format(path))

def find_media_files(working_dir, ignored_dirs=["BL_proxy"]):
    """
    Walks all files and folders from the working_dir
    except in ignored_dirs and returns a list of
    media file paths: pictures and videos the script can
    generate a proxy for
    """
    file_paths = []
    FILE_EXTENSIONS = list(Video.EXTENSIONS + Image.EXTENSIONS)
    for dirpath, dirnames, filenames in os.walk(working_dir):
        tail = os.path.split(dirpath)[1]
        if tail in ignored_dirs:
            dirnames[:] = []
            continue

        for f in filenames:
            file_path = os.path.join(dirpath, f)
            extension = os.path.splitext(file_path)[1]
            if extension.lower() in FILE_EXTENSIONS:
                file_paths.append(os.path.join(dirpath, f))
    return file_paths

OPTIONS_PRESETS = dict()

def get_command_line_arguments():
    parser = argparse.ArgumentParser(description="Create proxies for Blender VSE using FFMPEG.")
    parser.add_argument("working_directory", nargs="?", default=".",
                        help="The directory containing media to create proxies for")
    parser.add_argument("-p", "--preset", help="A preset name for proxy encoding",
                        choices=[])
    return parser.parse_args()

def create_media(path_list):
    """
    Takes a list of media file paths and builds Video or Image objects
    depending on their extensions
    Returns a list of Media objects (Video and Image objects)
    """
    medias = []
    for path in path_list:
        if Video.is_same_type(path):
            medias.append(Video(path, **options))
        elif Image.is_same_type(path):
            medias.append(Image(path, **options))

if __name__ == "__main__":
    """
    1) Parse arguments to get the working directory and encoding presets
    2) Find video and image files and create a Media object for each of them
    3) create proxy
        - create path
        - issue ffmpeg command and print progress
    """
    args = get_command_line_arguments()
    working_dir = get_working_directory(args.working_directory)
    options = dict()
    if args.preset:
        options = OPTIONS_PRESETS[args.preset]

    media_objects = create_media(find_media_files(working_dir))
    total = len(media_objects)
    print("found %d file(s) to convert" % total)
    for media in media_objects:
        print("~~ %s" % media.path_source)

    count = 1
    for media in media_objects:
        print("%d/%d :: %s" % (count, total, media.path_source))
        media.create_proxy_directory()
        media.create_proxy_file()
        count += 1
