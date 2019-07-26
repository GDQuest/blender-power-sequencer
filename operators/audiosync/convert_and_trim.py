import os
import subprocess
import tempfile


def convert_and_trim(audio_filepath, freq, dur):
    """
    Uses ffmpeg to convert an audio file to a temporary wav file for use
    in finding offset.

    Args
        :audio: path to the audiofile to convert (string)
        :freq:  Samples / second in the output wav (int)
        :dur:   Max duration of the output wav in seconds (float)

    Returns
        :outpath: path to the output wav file
    """

    tmp = tempfile.NamedTemporaryFile(mode="r+b", prefix="offset_", suffix=".wav")
    outpath = tmp.name
    tmp.close()

    channel_count = "1"

    subprocess.call(
        [
            "ffmpeg",
            "-loglevel",
            "panic",
            "-i",
            audio_filepath,
            "-ac",
            channel_count,
            "-ar",
            str(freq),
            "-t",
            str(dur),
            "-acodec",
            "pcm_s16le",
            outpath,
        ]
    )

    return outpath
