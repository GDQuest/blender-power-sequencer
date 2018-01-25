import os
import subprocess
import sys
import logging


def parse_cmd_args():
    if len( sys.argv ) > 1:
        path = os.path.abspath(sys.argv[1])
        if not os.path.exists(path):
            return
        if os.path.isfile(path) and path.endswith('.blend'):
            path = os.path.split(path)[0]
        if not os.path.isdir(path):
            return
        return path

project_folder = parse_cmd_args()
if not project_folder:
    project_folder = '.'
    logging.warning('The folder passed as an argument isn\'t valid. Using the current folder instead')


VIDEO_EXT = ['.mp4', '.mkv', '.mov', '.flv']
IMG_EXT = ['.png', '.jpg', '.jpeg']

FFMPEG_VIDEO_COMMAND = ["ffmpeg", "-i", "", "-hide_banner", "-f", "matroska", "-sn", "-an", "-c:v", "mpeg2video", "-b:v", "1800k", "-filter:v", "scale=iw*0.25:ih*0.25", "-y", ""]
FFMPEG_IMAGE_COMMAND = ["ffmpeg", "-i", "", "-hide_banner", "-vf", "scale=iw*0.25:ih*0.25", ""]

ffmpeg_commands = []
img_proxy_folders = []
for dirpath, dirnames, filenames in os.walk(project_folder):
    found_image, found_video = False, False

    if 'BL_proxy' in dirpath:
        continue

    for f in filenames:
        file_path = os.path.join(dirpath, f)
        _, extension = os.path.splitext(f)

        if extension.lower() in VIDEO_EXT:
            video_proxy_subdir = os.path.join(dirpath, 'BL_proxy/{!s}/'.format(f))
            if not os.path.isdir(video_proxy_subdir):
                os.makedirs(video_proxy_subdir)

            new_command = [arg for arg in FFMPEG_VIDEO_COMMAND]
            new_command[2] = file_path
            new_command[-1] = os.path.join(video_proxy_subdir, 'proxy_25.avi')
            print(new_command)
            ffmpeg_commands.append(new_command)

        elif extension.lower() in IMG_EXT:
            img_proxy_folder = os.path.join(dirpath, 'BL_proxy/images/25/')
            if not found_image:
                if not os.path.isdir(img_proxy_folder):
                    os.makedirs(img_proxy_folder)
                img_proxy_folders.append(img_proxy_folder)
                found_image = True
            new_command = [arg for arg in FFMPEG_IMAGE_COMMAND]
            new_command[2] = file_path
            new_command[-1] = os.path.join(img_proxy_folder, f)
            print(new_command)
            ffmpeg_commands.append(new_command)

for command in ffmpeg_commands:
    process = subprocess.Popen(command)
    process.wait()

for folder in img_proxy_folders:
    # print(folder)
    for img in os.listdir(folder):
        file_path = os.path.join(folder, img)
        # print(file_path)
        os.rename(file_path, file_path + '_proxy.jpg')