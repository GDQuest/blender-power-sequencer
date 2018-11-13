import subprocess


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

