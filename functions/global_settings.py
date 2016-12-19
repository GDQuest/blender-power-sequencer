from enum import Enum


class ProjectSettings():
    RESOLUTION_X = 1920
    RESOLUTION_Y = 1080
    PROXY_RESOLUTION_X = 640
    PROXY_RESOLUTION_Y = 360
    PROXY_STRING = "_proxy"

    class FOLDER_NAMES():
        AUDIO = 'audio'
        IMG = 'img'
        VIDEO = 'video'
        IMG_ASSETS = '-assets'
    folders = ()


ProjectSettings.folders = (
    ProjectSettings.FOLDER_NAMES.AUDIO,
    ProjectSettings.FOLDER_NAMES.IMG,
    ProjectSettings.FOLDER_NAMES.VIDEO,
    )


class FileTypes(Enum):
    """Tuples of file types for checks when importing files"""
    psd = "PSD"
    img = ("PNG", "JPG", "JPEG")
    audio = ("WAV", "MP3", "OGG")
    video = ("MP4", "AVI", "MTS")


class SequenceTypes():
    VIDEO = ('MOVIE', 'MOVIECLIP', 'META', 'SCENE')
    EFFECT = ('CROSS', 'ADD', 'SUBTRACT', 'ALPHA_OVER', 'ALPHA_UNDER', 'GAMMA_CROSS', 'MULTIPLY', 'OVER_DROP', 'WIPE', 'GLOW', 'TRANSFORM', 'COLOR', 'SPEED', 'ADJUSTMENT', 'GAUSSIAN_BLUR')
    SOUND = ('SOUND')
    IMAGE = ('IMAGE')

# TODO: Replace FileTypes with that
class Extensions():
    """Tuples of file types for checks when importing files"""
    PSD = ("*.psd")
    IMG = ("*.png", "*.jpg", "*.jpeg")
    AUDIO = ("*.wav", "*.mp3", "*.ogg")
    VIDEO = ("*.mp4", "*.avi", "*.mts")


# TODO: Replace RenderDim and Encoding with that
class RENDER_SETTINGS():
    """A list of tuples representing X, Y, resolution percentage, pixel ratio X, Y, FPS and FPS base parameters to use for rendering"""

    class RESOLUTION():
        HD_FULL = (1920, 1080, 100, 1, 1, 24, 1)
        HD_READY = (1280, 720, 100, 1, 1, 24, 1)

    class ENCODING():
        MP4_HIGH = ('H264', 'MPEG4', 'H264', 18, 9000, 9000, 0, 224 * 8,
                   2048, 10080000, 'AAC', 192)
        MP4_LOW = ('H264', 'MPEG4', 'H264', 18, 6000, 6000, 0, 224 * 8,
                    2048, 10080000, 'AAC', 192)


class SearchMode():
    NEXT = 1
    CHANNEL = 2
    ALL = 3
