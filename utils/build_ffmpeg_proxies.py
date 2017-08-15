import os
from subprocess import call

# Create a BL_proxy directory in each directory containing either pictures or movie files
# Don't re-create proxies if they already exist
# Upon generating a proxy, save the file path and update the time stamp

VIDEO_TYPES = ['.mkv']
IMAGE_TYPES = ['']

files = []

# Gather files to generate proxies for and create BL_proxy dirs
for dirpath, _, filenames in os.walk('.'):
    for f in filenames:
        file_name, file_extension = os.path.splitext(f)
        abs_dir = os.path.abspath(dirpath)
        if file_extension in IMAGE_TYPES or file_extension in VIDEO_TYPES:
            files.append(os.path.join(abs_dir, f))

# Make proxy dirs before generating proxies
for filepath in files:
    dirpath, filename = os.path.split(filepath)
    _, extension = os.path.splitext(filename)

    bl_proxy_folder = os.path.join(dirpath, 'BL_proxy')
    if not os.path.exists(bl_proxy_folder):
        os.mkdir(bl_proxy_folder)

    proxy_folder = os.path.join(bl_proxy_folder, filename)
    print(proxy_folder)
    if not os.path.exists(proxy_folder):
        os.mkdir(proxy_folder)

    # ffmpeg build
    # TODO: add support for different proxy sizes
    # TODO: add support for img files
    export_path = os.path.join(proxy_folder, 'proxy_25.avi')
    ffmpeg_command = ''
    if extension in VIDEO_TYPES:
        ffmpeg_command = "ffmpeg -i {!s} -strict experimental -hide_banner -f matroska -map_chapters -1 -map 0:0 -sn -an -c:v:0 mpeg2video -b:v:0 1800k -mbd:v:0 rd -mbcmp:v:0 rd -cmp:v:0 rd -precmp:v:0 rd -subcmp:v:0 rd -trellis:v:0 1 -filter:v:0 \"scale=480:270\" -y {!s}".format(filepath, export_path)
    # elif extension in IMAGE_TYPES:
    #     ffmpeg_command = "ffmpeg -i {!s} -vf \"scale=480:270\" {!s}".format("\"" + f + "\"", "\"" + "BL_proxy/" + f + "/proxy_25.png" + "\"")

    call(ffmpeg_command, shell=True)


