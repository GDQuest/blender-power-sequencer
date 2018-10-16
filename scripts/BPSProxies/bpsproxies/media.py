"""
Collection of objects to represent supported media sources: Video and Image
The objects store rendering options and can create and call commands to render proxies
with ffmpeg, using the subprocess module
"""
import os
import subprocess
import multiprocessing
from .presets import PRESETS
from .utils import get_frame_count

class Media:
    """
    Base interface to generate proxies with ffmpeg
    """
    EXTENSIONS = []

    def __init__(self, path_source, options):
        self.path_source = path_source
        self.proxy_command = []
        self.path_proxy = ''
        self.options = options

    @classmethod
    def is_same_type(cls, file_path):
        """
        Returns true if the file extension matches one of the class's EXTENSIONS
        """
        return os.path.splitext(file_path)[1].lower() in cls.EXTENSIONS

    def create_proxy_directory(self):
        """
        Create a BL_proxy folder relative to the file,
        where the final proxy will be stored
        """
        proxy_folder = os.path.split(self.path_proxy)[0]
        if not os.path.isdir(proxy_folder):
            os.makedirs(proxy_folder)

    def render_proxy_file(self):
        """
        Calls ffmpeg to render the proxy, using the object's own render command
        """
        process = subprocess.Popen(
            self.proxy_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True)
        process.wait()
        print("progress: 100%\n")


class Video(Media):
    """
    Represents a video
    """
    EXTENSIONS = [".mp4", ".mkv", ".mov", ".flv", ".mts"]

    def __init__(self, path_source, options):
        super().__init__(path_source, options)

        self.path_proxy = self.get_path_proxy(self.path_source)
        self.frame_count = get_frame_count(self.path_source)
        self.proxy_command = self.get_proxy_command(self.path_source,
                                                    self.path_proxy)

    def get_path_proxy(self, path):
        """
        Returns path the proxy file should be located
        """
        folder, file_name = os.path.split(path)
        return os.path.join(folder, "BL_proxy", file_name,
                            "proxy_{}.avi".format(self.options["size"]))

    def get_proxy_command(self, path_source, path_proxy):
        """
        Returns the ffmpeg command to generate a proxy file with the command line
        See this post to understand all the options below:
        https://github.com/GDquest/Blender-power-sequencer/issues/174#issuecomment-420586813
        """
        encoding_speed_key = self.options['encoding_speed']['key']
        encoding_speed_value = self.options['encoding_speed']['value']
        crf_key = self.options['constant_rate_factor']['key']
        crf_value = self.options['constant_rate_factor']['value']
        ffmpeg_command = [
            "ffmpeg",
            "-i", path_source,
            "-pix_fmt", "yuv420p",
            "-c:v", self.options["codec"],
            crf_key, crf_value,
            "-g", "1",
            encoding_speed_key, encoding_speed_value,
            "-vf", "colormatrix=bt601:bt709",
            "-filter:v", "scale=iw*{size}:ih*{size}".format(size=self.options["size"]/100),
            "-sn", "-an", "-v", "quiet", "-stats", "-y"]
        if self.options['format'] == 'webm':
            ffmpeg_command += ["-threads", str(multiprocessing.cpu_count())]
        ffmpeg_command.append(path_proxy)
        return ffmpeg_command

    def render_proxy_file(self):
        """
        Overrides render_proxy_file from Media
        """
        process = subprocess.Popen(
            self.proxy_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True)

        for line in process.stdout:
            progress = int(line[line.index("=") + 2:line.index(" f")].strip())
            percent = "{:.0%}".format(progress / self.frame_count)
            print("progress: %s" % percent, end="\r")
        process.wait()
        print("progress: 100%\n")


class Image(Media):
    """
    Represents an image
    """

    EXTENSIONS = [".png", ".jpg", ".jpeg"]

    def __init__(self, path_source, options):
        super().__init__(path_source, options)
        self.path_proxy = self.get_path_proxy(self.path_source)
        self.proxy_command = self.get_proxy_command(self.path_source,
                                                    self.path_proxy)

    def get_path_proxy(self, path):
        """
        takes in path to file, returns path the proxy file should be located
        """
        folder, file_name = os.path.split(path)
        return os.path.join(folder, "BL_proxy", "images",
                            str(self.options["size"]), file_name + "_proxy.jpg")

    def get_proxy_command(self, path_source, path_proxy):
        """
        takes in path to file, returns the command for generating the proxy
        """
        proxy_cmd = [
            "ffmpeg",
            "-i",
            path_source,
            "-v",
            "quiet",
            "-stats",
            "-f",
            "apng",
            "-filter:v",
            "scale=iw*{size}:ih*{size}".format(size=self.options["size"]/100),
            "-y",
            path_proxy,
        ]
        return proxy_cmd
