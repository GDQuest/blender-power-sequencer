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
    """
    Tuples of identifiers to check if a strip is of a certain type or type group
    """
    VIDEO = ('MOVIE', 'MOVIECLIP', 'META', 'SCENE')
    EFFECT = ('CROSS', 'ADD', 'SUBTRACT', 'ALPHA_OVER', 'ALPHA_UNDER',
              'GAMMA_CROSS', 'MULTIPLY', 'OVER_DROP', 'WIPE', 'GLOW',
              'TRANSFORM', 'COLOR', 'SPEED', 'ADJUSTMENT', 'GAUSSIAN_BLUR')
    TRANSITION = ('CROSS', 'GAMMA_CROSS', 'WIPE')
    SOUND = ('SOUND',)
    IMAGE = ('IMAGE',)
    TRANSITIONABLE = VIDEO + IMAGE + ('MULTICAM',)
    # Strips that can be cut. If most effect strips are linked to their inputs
    # and shouldn't be cut, some can be edited directly
    CUTABLE = VIDEO + SOUND + IMAGE + ('MULTICAM', 'COLOR', 'ADJUSTMENT')


# TODO: Replace FileTypes with that
class Extensions():
    """
    Tuples of file types for checks when importing files
    Attributes:
        DICT: A dictionary of file types. Each key (IMG, AUDIO, VIDEO, PSD) contains a set
        of strings that represent a file name with a wildcard and extension ("*.ext"). To
        use with the glob builtin module.
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
