import os
import subprocess

import argparse
import sys

class Media:
    """
    Base interface to generate proxies from with ffmpeg
    """

    def __init__(self, path_source, **kwargs):
        self.path_source = path_source
        self.options = kwargs

        if "size" not in self.options:
            self.options["size"] = 25

    @classmethod
    def is_same_type(cls, file_path):
        return os.path.splitext(path)[1].lower() in cls.EXTENSIONS

    def create_proxy_directory(self):
        """
        creates the directory for the proxy
        """
        proxy_folder = os.path.split(self.path_proxy)[0]
        if not os.path.isdir(proxy_folder):
            os.makedirs(proxy_folder)

    def create_proxy_file(self):
        """
        calls ffmpeg to generate proxy
        """
        process = subprocess.Popen(
            self.proxy_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True)
        process.wait()
        print("progress: 100%")
        print("Done!", "\n")


class Video(Media):
    """
    Represents a video
    """
    EXTENSIONS = [".mp4", ".mkv", ".mov", ".flv", ".mts"]

    def __init__(self, path_source, **kwargs):
        super().__init__(path_source, **kwargs)
        if "codec" not in self.options:
            self.options["codec"] = ""
        if "crf" not in self.options:
            self.options["crf"] = "25"

        self.path_proxy = self.get_path_proxy(self.path_source)
        self.frame_count = self.get_frame_count(self.path_source)
        self.proxy_command = self.get_proxy_command(self.path_source,
                                                    self.path_proxy)

    def get_frame_count(self, path):
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
            path,
        ]
        return int(subprocess.check_output(ffprobe_frame_cmd).decode())

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
        """
        proxy_cmd = [
            "ffmpeg",
            "-i",
            path_source,
            "-c:v",
            self.options["codec"],
            "-crf",
            self.options["crf"],
            "-filter:v",
            "scale=iw*{size}:ih*{size}".format(size = self.options["size"]/100),
            "-sn", "-an", "-v", "quiet", "-stats", "-y",
            path_proxy,
        ]
        return proxy_cmd

    def create_proxy_file(self):
        """
        Overrides create_proxy_file from Media
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
        print("progress: 100%")
        print("Done!", "\n")


class Image(Media):
    """
    Represents an image
    """

    EXTENSIONS = [".png", ".jpg", ".jpeg"]

    def __init__(self, path_source, **kwargs):
        super().__init__(path_source, **kwargs)
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
            "scale=iw*{size}:ih*{size}".format(size = self.options["size"]/100),
            "-y",
            path_proxy,
        ]
        return proxy_cmd
