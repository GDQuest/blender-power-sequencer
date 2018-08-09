import argparse
import os
import subprocess
import sys


class Media:
    """
    Base interface to generate proxies from with ffmpeg
    """
    EXTENSIONS = ["test"]

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
    EXTENSIONS = [".mp4", ".mkv", ".mov", ".flv"]

    def __init__(self, path_source, **kwargs):
        super().__init__(path_source, **kwargs)
        if "codec" not in self.options:
            self.options["codec"] = "mpeg2video"
        if "bitrate" not in self.options:
            self.options["bitrate"] = "1800k"

        self.path_proxy = self.get_path_proxy(self.path_source)
        self.frame_count = self.get_frame_count(self.path_source)
        self.proxy_command = self.get_proxy_command(self.path_source,
                                                    self.path_proxy)

    def get_frame_count(self, path):
        """
        takes in path to file, returns the number of frames in the video
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
        takes in path to file, returns path the proxy file should be located
        """
        folder, file_name = os.path.split(path)
        return os.path.join(folder, "BL_proxy", file_name,
                            "proxy_{}.avi".format(self.options["size"]))

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
            "matroska",
            "-sn",
            "-an",
            "-c:v",
            self.options["codec"],
            "-b:v",
            self.options["bitrate"],
            "-filter:v",
            "scale=iw*{size}:ih*{size}".format(size = self.options["size"]/100),
            "-y",
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


def get_working_directory(path):
    """
    If path is an actually directory its absolute path is returned. If it is a
    .blend file the absolute path to the containing directory is returned. In
    all other cases an exception is raised.
    """
    abs_path = os.path.abspath(path)
    if os.path.exists(abs_path):
        if os.path.isdir(abs_path):
            return abs_path
        elif os.path.isfile(abs_path) and abs_path.endswith(".blend"):
            return os.path.dirname(abs_path)
    raise ValueError("{} is neither a directory nor a .blend file".format(path))

def get_media_file_paths(working_dir, ignored_dirs=["BL_proxy"]):
    """
    Walks all files and folders from the working_dir
    except in ignored_dirs and returns a list of
    media file paths: pictures and videos the script can
    generate a proxy for
    """
    file_paths = []
    FILE_EXTENSIONS = list(Video.EXTENSIONS + Image.EXTENSIONS)
    for dirpath, dirnames, filenames in os.walk(working_dir):
        tail = os.path.split(dirpath)[1]
        if tail in ignored_dirs:
            dirnames[:] = []
            continue

        for f in filenames:
            file_path = os.path.join(dirpath, f)
            extension = os.path.splitext(file_path)[1]
            if extension.lower() in FILE_EXTENSIONS:
                file_paths.append(os.path.join(dirpath, f))
    return file_paths

OPTIONS_PRESETS = dict()

if __name__ == "__main__":
    """
    1) Parse arguments to get the working directory and encoding presets
    2) Find video and image files and create a Media object for each of them
    3) create proxy
        - create path
        - issue ffmpeg command and print progress
    """

    parser = argparse.ArgumentParser(description="Create proxies for Blender VSE using FFMPEG.")
    parser.add_argument("working_directory", nargs="?",
                        help="The directory containing media to create proxies for")
    parser.add_argument("-p", "--preset", help="A preset name for proxy encoding",
                        choices=[])
    args = parser.parse_args()

    working_dir = "."
    if args.working_directory:
        working_dir = get_working_directory(args.working_directory)

    media_file_paths = get_media_file_paths(working_dir)

    options = dict()
    if args.preset:
        options = OPTIONS_PRESETS[args.preset]

    media_objects = []
    for path in media_file_paths:
        if Video.is_same_type(path):
            media_objects.append(Video(path, **options))
        elif Image.is_same_type(path):
            media_objects.append(Image(path, **options))

    total = len(media_objects)
    print("found %d file(s) to convert" % total)
    for media in media_objects:
        print("~~ %s" % media.path_source)

    count = 1
    for media in media_objects:
        print()
        print("%d/%d :: %s" % (count, total, media.path_source))
        media.create_proxy_directory()
        media.create_proxy_file()
        count += 1
