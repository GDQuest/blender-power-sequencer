import os
from subprocess import call

# Create a BL_proxy directory in each directory containing either pictures or movie files
# Don't re-create proxies if they already exist
# Upon generating a proxy, save the file path and update the time stamp

# Gather files to generate proxies for and create BL_proxy dirs
video_files, image_files = [], []
for dirpath, _, filenames in os.walk('.'):
    for f in filenames:
        file_name, file_extension = os.path.splitext(f)
        if file_extension in IMAGE_TYPES:
            image_files.append(os.path.join(dirpath, f))
        elif file_extension in VIDEO_TYPES:
            video_files.append(os.path.join(dirpath, f))

# Make proxy dirs before generating proxies
all_files = video_files.extend(image_files)
for f in all_files:
    dirpath, filename = os.path.splitext(f)
    bl_proxy_folder = os.path.join(dirpath, 'BL_proxy')
    if not os.path.isdir(bl_proxy_folder):
        os.mkdir(bl_proxy_folder)


for f in video_files:
    ffmpeg_command = "ffmpeg -i {!s} -strict experimental -hide_banner -f matroska -map_chapters -1 -map 0:0 -sn -an -c:v:0 mpeg2video -b:v:0 1800k -mbd:v:0 rd -mbcmp:v:0 rd -cmp:v:0 rd -precmp:v:0 rd -subcmp:v:0 rd -trellis:v:0 1 -filter:v:0 \"scale=480:270\" -y {!s}".format("\"" + f + "\"", "\"" + "BL_proxy/" + f + "/proxy_25.avi" + "\"")
    call(ffmpeg_command, shell=True)

# TODO: Check image proxy expected filename - we likely have to build as png and rename it
for f in image_files:
    ffmpeg_command = "ffmpeg -i {!s} -vf \"scale=480:270\" {!s}".format("\"" + f + "\"", "\"" + "BL_proxy/" + f + "/proxy_25.png" + "\"")
    call(ffmpeg_command, shell=True)
