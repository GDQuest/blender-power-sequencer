import os
import subprocess
import sys
import logging


EXT_VIDEO = ['.mp4', '.mkv', '.mov', '.flv']
EXT_IMG = ['.png', '.jpg', '.jpeg']

TYPE_VIDEO = "video"
TYPE_IMG = "img"

FFMPEG_COMMAND_VIDEO = ["ffmpeg", "-i", "", "-v", "quiet", "-stats", "-f", "matroska", "-sn", "-an", "-c:v", "mpeg2video", "-b:v", "1800k", "-filter:v", "scale=iw*0.25:ih*0.25", "-y", ""]
FFMPEG_COMMAND_IMG = ["ffmpeg", "-i", "", "-v", "quiet", "-stats", "-vf", "scale=iw*0.25:ih*0.25", "-y", ""]
FFPROBE_COMMAND_VIDEO = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames", "-of", "default=noprint_wrappers=1:nokey=1", ""]


def parse_cmd_args():
    """
    Finds and returns the path to the folder passed
    as a command line argument, if it exists
    """
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
    FILE_EXTENSIONS = list(EXT_VIDEO + EXT_IMG)
    for dirpath, dirnames, filenames in os.walk(project_folder):
        head, tail = os.path.split(dirpath)
        if tail in ignored_folder_names:
            dirnames[:] = []
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
    a local proxy folder: the output file path to pass to ffmpeg

    That's the path Blender will look for file proxies
    e.g. for "video/shot_1.mov", the function returns
    "video/BL_proxy/shot_1.mov/proxy_25.avi"
    """
    folder, file_name = os.path.split(source_file_path)
    extension = os.path.splitext(file_name)[1].lower()
    if extension in EXT_VIDEO:
        return os.path.join(folder, 'BL_proxy', file_name, "proxy_25.avi")
    elif extension in EXT_IMG:
        return os.path.join(folder, 'BL_proxy', 'images', '25', file_name)
    return ''


def get_file_type(path):
    """
    returns the type of a file, TYPE_*
    """
    path, extension = os.path.splitext(path)
    return TYPE_IMG if extension.lower() in EXT_IMG else TYPE_VIDEO


def make_proxy_command(src_file_path, proxy_base_path):
    """
    Takes a template FFMPEG_COMMAND_* and returns the full argument list
    to call with subprocess.Popen
    """
    src_file_type = get_file_type(src_file_path)
    command_template = FFMPEG_COMMAND_VIDEO if src_file_type == TYPE_VIDEO else FFMPEG_COMMAND_IMG

    command = [arg for arg in command_template]
    command[2] = src_file_path
    if src_file_type == TYPE_VIDEO:
        command[-1] = proxy_base_path
    elif src_file_type == TYPE_IMG:
        command[-1] = proxy_base_path + "_proxy.jpg"
    return command


def run_commands(commands):

    map_video_nb_frame = {}

    total = len(commands)
    print("found %d file(s) to convert" % total)
    for c in commands:
        print('~~ %s' % c[2])
        if get_file_type(c[2]) == TYPE_VIDEO:
            probe_frame_cmd = [arg for arg in FFPROBE_COMMAND_VIDEO]
            probe_frame_cmd[-1] = c[2]
            map_video_nb_frame[c[2]] = int(subprocess.check_output(probe_frame_cmd).decode())
    print()

    count = 1
    for c in commands:
        print("%d/%d :: %s" % (count, total, c[2]))
        process = subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
        if get_file_type(c[2]) == TYPE_VIDEO:
            for line in process.stdout:
                progress = int( line[line.index('=')+2 : line.index(' f')].strip())
                percent = '{:.0%}'.format(progress / map_video_nb_frame.get(c[2], progress))
                print('progress: %s' % percent, end='\r')
        process.wait()
        print('progress: 100%')
        print('Done!', '\n')
        count +=1


# SCRIPT
project_folder = parse_cmd_args()
if not project_folder:
    project_folder = '.'
    logging.warning('The folder passed as an argument isn\'t valid. Using the current folder instead')

commands = []
media_files = get_media_file_paths(project_folder)
for f in media_files:
    proxy_file_path = get_proxy_file_path(f)
    command = make_proxy_command(f, proxy_file_path)

    proxy_folder_path = os.path.split(proxy_file_path)[0]
    if not os.path.isdir(proxy_folder_path):
        os.makedirs(proxy_folder_path)
    commands.append(command)

run_commands(commands)
