"""
Collection of utility functions, class-independent
"""
import subprocess

def get_frame_count(media_file_path):
    """
    Returns the number of frames in the video, using the ffprobe program
    """
    ffprobe_frame_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=nb_frames",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        media_file_path,
    ]
    return int(subprocess.check_output(ffprobe_frame_cmd).decode())
