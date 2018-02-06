import bpy
from bpy_extras.io_utils import ImportHelper

import os
import subprocess
from mimetypes import MimeTypes
from urllib import request


class BatchTranscode(bpy.types.Operator, ImportHelper):
    """
    Batch Transcode videos to a specific framerate.

    Select which files to transcode, frame rate, and whether or not to
    include audio. New video files are generated for all video files
    that are not currently using the desired frame rate.

    This operator is available in the user interface only.
    """

    bl_idname = "power_sequencer.batch_transcode"
    bl_label = "Batch Transcode"
    bl_description = "Transcode a list of selected video files to a frame rate"

    fps_options = [
        ("23.98", "23.98", ""),
        ("24", "24", ""),
        ("25", "25", ""),
        ("29.97", "29.97", ""),
        ("30", "30", ""),
        ("50", "50", ""),
        ("59.94", "59.94", ""),
        ("60", "60", ""),
        ("120", "120", ""),
    ]

    fps = bpy.props.EnumProperty(
        items=fps_options,
        name="FPS Options",
        default="24",
    )

    include_audio = bpy.props.BoolProperty(
        name="Include Audio",
        default=True
    )

    files = bpy.props.CollectionProperty(
        name='File paths',
        type=bpy.types.OperatorFileListElement
    )

    def execute(self, context):
        if not is_ffmpeg_available():
            message = "You must have ffmpeg installed to use this operator"
            self.report({'ERROR'}, message)
            return {'FINISHED'}

        current_framerates = {}

        folder = os.path.dirname(self.filepath)
        for file in sorted(self.files, key=lambda f: f.name):
            filepath = os.path.join(folder, file.name)

            if is_video(filepath):
                print(filepath)
                current_framerates[filepath] = get_framerate(filepath)

        actual_fps = {
            "23.98": 24 / 1.001,
            "24": 24,
            "25": 25,
            "29.97": 30 / 1.001,
            "30": 30,
            "50": 50,
            "59.54": 60 / 1.001,
            "60": 60,
            "120": 120
        }

        converted_files = []
        fps = actual_fps[self.fps]
        for key in current_framerates.keys():
            if not round(current_framerates[key], 1) == round(fps, 1):
                transcode(key, fps, self.include_audio)
                converted_files.append(key)

        if len(converted_files) > 1:
            self.report(
                {"INFO"},
                "%s files were transcoded" % str(len(converted_files)))
        else:
            self.report(
                {"INFO"},
                "%s file was transcoded" % str(len(converted_files)))

        return {'FINISHED'}


def get_framerate(filepath):
    """
    Use ffmpeg to get the frame rate for the given file

    Parameters
    ----------
    filepath : str

    Returns
    -------
    framerate : float
    """
    report = subprocess.Popen(
        ['ffmpeg', '-i', filepath],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    output, error = report.communicate()

    # We use the error because ffmpeg complains about no output file.
    message = error.decode('utf-8')

    pre = message.split('fps')[0]
    number = pre.split(',')[-1].strip()

    fps = float(number)

    return fps


def is_ffmpeg_available():
    """
    Check if ffmpeg is installed and usable

    Returns
    -------
    bool
    """
    try:
        subprocess.call(
            ['ffmpeg', '--help'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        return True

    except OSError:
        return False


def is_video(filepath):
    """
    Check if a file is a video file

    Parameters
    ----------
    filepath : str

    Returns
    -------
    bool
    """
    mime = MimeTypes()
    url = request.pathname2url(filepath)
    mime_type = mime.guess_type(url)

    if "video" in str(mime_type):
        return True

    return False


def transcode(filepath, fps, include_audio):
    """
    Transcode a video file to avi raw

    Parameters
    ----------
    filepath : str
    fps : float
    include_audio : bool
    """

    folder = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    output_name = ''.join(
        ['(transcoded) ', os.path.splitext(filename)[0], '.avi'])
    output_path = os.path.join(folder, output_name)

    if include_audio:
        subprocess.call(
            ['ffmpeg',
             '-i', filepath,
             '-r', str(fps),
             '-loglevel', 'panic',
             '-vcodec', 'rawvideo',
             '-acodec', 'pcm_s16le',
             '-y',
             output_path])

    else:
        subprocess.call(
            ['ffmpeg',
             '-i', filepath,
             '-r', str(fps),
             '-loglevel', 'panic',
             '-vcodec', 'rawvideo',
             '-y',
             output_path])
