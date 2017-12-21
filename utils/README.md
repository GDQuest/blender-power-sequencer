# Power Sequencer Utils

This folder contains extra tools to help develop the add-on or to help work with the add-on, but not as part of blender.

## Build better proxies faster with FFMpeg


The `build_ffmpeg_proxies.py` script generates 25% proxies for Blender with ffmpeg in batch. It walks through your project folder or any folder tree and finds videos and image files.
It only looks for the file types in VIDEO_EXT and IMG_EXT.

*Feel free to upload a PR to improve this script and add more features. I can help you get started if you need.*

At the moment it only support 25% proxy generation. For HD and 4k video, I find it's the only size that always gives good performance. 50% of a 4k video is 1920*1080 after all, which is huge to preview on one CPU core like Blender does.

How to use:

- Open the script from the shell like `python build_ffmpeg_proxies.py project_folder`
- The project_folder should be the path to a folder that contains all the files you want to proxy.

You must have ffmpeg installed and available from the command line. Write ffmpeg -v in the shell to check if it's globally available.

The script uses the mpeg-2 video codec. It produces small and clean video files with decent performance in Blender. The result is of a much higher quality than the mjpeg proxies blender generates by default, and takes far less space on your drive.
For images, it respects the original format and transparency, unlike the built-in proxy system.

### Possible improvements

- Use last file changed/timestamp and only rebuild proxies on files that changed
- Add support for more file formats
- Add option or script to clear/remove proxies
- Add a hook in the add-on to run the script from within Blender, with progress logging

### Extra ideas

- Add an optional cli option to generate to a different proxy size (25%, 50%, 100%)
- Add an optional cli option for more efficient codec for performance, size? E.g. h264 and ProRes?
- Currently local proxies only. add an optional master proxy folder to dump all the files? NB: Not a big fan of this. Although it's easier to delete them later or this lets you share them with your team on a server the folder soon becomes cluttered. One master folder with sub-folder per project would be ideal, but it requires more work.
