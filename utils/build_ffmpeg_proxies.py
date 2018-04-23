import os
import subprocess
import sys
import logging


VIDEO_EXT = ['.mp4', '.mkv', '.mov', '.flv']
IMG_EXT = ['.png', '.jpg', '.jpeg']

FFMPEG_VIDEO_COMMAND = ["ffmpeg", "-i", "", "-hide_banner", "-f", "matroska", "-sn", "-an", "-c:v", "mpeg2video", "-b:v", "1800k", "-filter:v", "scale=iw*0.25:ih*0.25", "-y", ""]
FFMPEG_IMAGE_COMMAND = ["ffmpeg", "-i", "", "-hide_banner", "-vf", "scale=iw*0.25:ih*0.25", ""]


def parse_cmd_args():
    if len(sys.argv) > 1:
        path = os.path.abspath(sys.argv[1])
        if not os.path.exists(path):
            return
        if os.path.isfile(path) and path.endswith('.blend'):
            path = os.path.split(path)[0]
        if not os.path.isdir(path):
            return
        return path


def get_media_file_paths(base_project_folder, ignored_folder_names=['BL_proxy']):
    """
    Walks all files and folders from the base_project_folder
    except in ignored_folders and returns a list of
    media file paths, pictures and videos the script can
    generate a proxy for
    """
    files = []
    FILE_EXTENSIONS = list(VIDEO_EXT + IMG_EXT)
    for dirpath, dirnames, filenames in os.walk(project_folder):
        for name in ignored_folder_names:
            if name in dirpath:
                continue

        for f in filenames:
            file_path = os.path.join(dirpath, f)
            extension = os.path.splitext(file_path)[1]
            if extension.lower() in FILE_EXTENSIONS:
                files.append(os.path.join(dirpath, f))
    return files


def get_proxy_file_path(source_file_path):
    """
    Takes a source path, relative or absolute, and returns
    a local proxy folder and file path to pass to ffmpeg
    That's the path Blender will look for file proxies
    e.g. for "video/shot_1.mov", the function returns
    "video/BL_proxy/shot_1.mov/proxy_25.avi"
    """
    folder, file_name = os.path.split(source_file_path)
    extension = os.path.splitext(file_name)[1]
    if extension in VIDEO_EXT:
        return os.path.join(folder, 'BL_proxy', file_name, 'proxy_25.avi')
    elif extension in IMG_EXT:
        return os.path.join(folder, 'BL_proxy', 'images', '25', file_name)
    return ''


# def make_proxy_command():
#     if not os.path.isdir(video_proxy_subdir):
#         os.makedirs(video_proxy_subdir)

#     new_command = [arg for arg in FFMPEG_VIDEO_COMMAND]
#     new_command[2] = file_path
#     new_command[-1] = os.path.join(video_proxy_subdir, 'proxy_25.avi')
#     print(new_command)
#     ffmpeg_commands.append(new_command)

#     if extension.lower() in IMG_EXT:
#         img_proxy_folder = os.path.join(dirpath, 'BL_proxy', 'images', '25')
#         if not found_image:
#             if not os.path.isdir(img_proxy_folder):
#                 os.makedirs(img_proxy_folder)
#             img_proxy_folders.append(img_proxy_folder)
#             found_image = True
#         new_command = [arg for arg in FFMPEG_IMAGE_COMMAND]
#         new_command[2] = file_path
#         new_command[-1] = os.path.join(img_proxy_folder, f)
#         print(new_command)
#         ffmpeg_commands.append(new_command)


def generate_proxies_with_ffmpeg(commands):
    for command in commands:
        process = subprocess.Popen(command)
        process.wait()


# SCRIPT
project_folder = parse_cmd_args()
if not project_folder:
    project_folder = '.'
    logging.warning('The folder passed as an argument isn\'t valid. Using the current folder instead')

media_files = get_media_file_paths(project_folder)
print(media_files)
for f in media_files:
    print(get_proxy_file_path(f))

# Generate commands
# Build proxies
# Generate timestamp
# Store a dict with the data
# Convert to JSON (see import local footage)
# Save JSON to disk
sys.exit()

# for folder in img_proxy_folders:
#     for img in os.listdir(folder):
#         file_path = os.path.join(folder, img)
#         os.rename(file_path, file_path + '_proxy.jpg')
