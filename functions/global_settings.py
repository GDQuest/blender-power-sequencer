from enum import Enum
import bpy


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

    def __dir__(self):
        return self.FOLDER_NAMES.AUDIO, self.FOLDER_NAMES.IMG, self.FOLDER_NAMES.VIDEO


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

    DICT = {
        "IMG": ("*.png", "*.jpg", "*.jpeg"),
        "AUDIO": ("*.wav", "*.mp3", "*.ogg"),
        "VIDEO": ("*.mp4", "*.avi", "*.mts")
    }


# TODO: Replace RenderDim and Encoding with that
class RENDER_SETTINGS():
    """A list of tuples representing X, Y, resolution percentage, pixel ratio X, Y, FPS and FPS base parameters to use for rendering"""

    class RESOLUTION():
        HD_FULL = (1920, 1080, 100, 1, 1, 24, 1)
        HD_READY = (1280, 720, 100, 1, 1, 24, 1)
        PROXY = (640, 368, 100, 1, 1, 24, 1)

    class ENCODING():
        MP4_HIGH = ('H264', 'MPEG4', 'H264', 18, 9000, 0, 0, 224 * 8,
                    2048, 10080000, 'AAC', 192)
        MP4_MEDIUM = ('H264', 'MPEG4', 'H264', 18, 6000, 0, 0, 224 * 8,
                   2048, 10080000, 'AAC', 192)
        MP4_PROXY = ('H264', 'MPEG4', 'H264', 18, 1500, 0, 0, 224 * 8,
                     2048, 10080000, 'AAC', 192)

# TODO: Create presets that can be accessed using the Enum parameter in the
# export operator as PRESETS[self.target][self.RESOLUTION] ?
# PRESETS = {
#     'youtube': {

#     },
#     'twitter': {

#     },
#     'facebook': {

#     },
#     'proxies': {

#     }
# }


class SearchMode():
    NEXT = 1
    CHANNEL = 2
    ALL = 3


class SequenceParams():
    """A reference to valid parameters to use on sequences with operator.attrgetter"""
    CHANNEL = 'channel'
    FRAME_START = 'frame_final_start'
    FRAME_END = 'frame_final_end'
    FRAME_DURATION = 'frame_final_duration'

    def __dir__(self):
        return self.CHANNEL, self.FRAME_DURATION, self.FRAME_END, self.FRAME_START