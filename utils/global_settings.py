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


class SequenceTypes():
    VIDEO = ['MOVIE', 'MOVIECLIP', 'META', 'SCENE']
    EFFECT = ['CROSS', 'ADD', 'SUBTRACT', 'ALPHA_OVER', 'ALPHA_UNDER',
              'GAMMA_CROSS', 'MULTIPLY', 'OVER_DROP', 'WIPE', 'GLOW',
              'TRANSFORM', 'COLOR', 'SPEED', 'ADJUSTMENT', 'GAUSSIAN_BLUR']
    SOUND = ['SOUND']
    IMAGE = ['IMAGE']


# TODO: Replace FileTypes with that
class Extensions():
    """
    Tuples of file types for checks when importing files
    Attributes:
        DICT: A dictionary of file types. Each key (IMG, AUDIO, VIDEO, PSD) contains a set of strings that represent a file name with a wildcard and extension ("*.ext"). To use with the glob builtin module.
    """
    DICT = {
        "IMG": ("*.png", "*.jpg", "*.jpeg"),
        "AUDIO": ("*.wav", "*.mp3", "*.ogg"),
        "VIDEO": ("*.mp4", "*.avi", "*.mts", "*.flv", "*.mkv", "*.mov"),
        "PSD": ("*.psd")
    }


class SearchMode():
    NEXT = 1
    CHANNEL = 2
    ALL = 3
