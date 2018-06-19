import os
import subprocess
import sys
import logging

class Video():
    '''
    Represents a video
    '''
    EXTS = ['.mp4', '.mkv', '.mov', '.flv']
    GEN_PROXY_TEMPL = ["ffmpeg", "-i", "", "-v", "quiet", "-stats", "-f", "matroska", "-sn", "-an", "-c:v", "mpeg2video", "-b:v", "1800k", "-filter:v", "scale=iw*0.25:ih*0.25", "-y", ""]
    PROBE_FRAMES_TEMPL = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames", "-of", "default=noprint_wrappers=1:nokey=1", ""]

    def __init__(self, path_orig):
        self.path_orig = path_orig
        self.num_frames = self.probe_frame(self.path_orig)
        self.path_proxy = self.gen_path_proxy(self.path_orig)
        self.proxy_command = self.gen_proxy_command(self.path_orig, self.path_proxy)

    @staticmethod
    def isVideo(path):
        return os.path.splitext(path)[1].lower() in Video.EXTS

    # takes in path to file, returns the number of frames in the video
    # warning: side effects
    def probe_frame(self, path):
        probe_frame_cmd = [arg for arg in self.PROBE_FRAMES_TEMPL]
        probe_frame_cmd[-1] = path
        return int(subprocess.check_output(probe_frame_cmd).decode())

    # takes in path to file, returns path the proxy file should be located
    def gen_path_proxy(self, path):
        folder, file_name = os.path.split(path)
        return os.path.join(folder, 'BL_proxy', file_name, "proxy_25.avi")
    
    # takes in path to file, returns the command for generating the proxy
    def gen_proxy_command(self, path_orig, path_proxy):
        proxy_cmd = [arg for arg in self.GEN_PROXY_TEMPL]
        proxy_cmd[2] = path_orig
        proxy_cmd[-1] = path_proxy
        return proxy_cmd

    # creates the directory for the proxy
    # warning: side effects
    def create_proxy_path(self):
        proxy_folder = os.path.split(self.path_proxy)[0]
        if not os.path.isdir(proxy_folder):
            os.makedirs(proxy_folder)

    # calls ffmpeg to generate proxy
    # warning: side effects
    def create_proxy_file(self):
        process = subprocess.Popen(self.proxy_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
        for line in process.stdout:
                progress = int( line[line.index('=')+2 : line.index(' f')].strip())
                percent = '{:.0%}'.format(progress / self.num_frames)
                print('progress: %s' % percent, end='\r')
        process.wait()
        print('progress: 100%')
        print('Done!', '\n')
        
class Image():
    '''
    Represents an image
    '''
    EXTS = ['.png', '.jpg', '.jpeg']
    GEN_PROXY_TEMPL = ["ffmpeg", "-i", "", "-v", "quiet", "-stats", "-vf", "scale=iw*0.25:ih*0.25", "-y", ""]
    
    def __init__(self, path_orig):
        self.path_orig = path_orig
        self.path_proxy = self.gen_path_proxy(self.path_orig)
        self.proxy_command = self.gen_proxy_command(self.path_orig, self.path_proxy)

    @staticmethod
    def isImage(path):
        return os.path.splitext(path)[1].lower() in Image.EXTS

    # takes in path to file, returns path the proxy file should be located
    def gen_path_proxy(self, path):
        folder, file_name = os.path.split(path)
        return os.path.join(folder, 'BL_proxy', 'images', '25', file_name)
    
    # takes in path to file, returns the command for generating the proxy
    def gen_proxy_command(self, path_orig, path_proxy):
        proxy_cmd = [arg for arg in self.GEN_PROXY_TEMPL]
        proxy_cmd[2] = path_orig
        proxy_cmd[-1] = path_proxy + "_proxy.jpg"
        return proxy_cmd

    # creates the directory for the proxy
    # warning: side effects
    def create_proxy_path(self):
        proxy_folder = os.path.split(self.path_proxy)[0]
        if not os.path.isdir(proxy_folder):
            os.makedirs(proxy_folder)

    # calls ffmpeg to generate proxy
    # warning: side effects
    def create_proxy_file(self):
        process = subprocess.Popen(self.proxy_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
        process.wait()
        print('progress: 100%')
        print('Done!', '\n')

# warning: side effects
def parse_cmd_args():
    """
    Finds and returns the path to the folder passed
    as a command line argument, if it exists
    Otherwise, logs an error, and uses the current directory
    """
    path = '.'
    if len(sys.argv) > 1:
        path_from_args = os.path.abspath(sys.argv[1])
        if os.path.exists(path_from_args):
            if os.path.isdir(path_from_args):
                path = path_from_args
            elif os.path.isfile(path_from_args) and path.endswith('.blend'):
                path = os.path.split(path)[0]
    return path

# warning: side effects 
def get_media_file_paths(working_dir, ignored_dirs=['BL_proxy']):
    """
    Walks all files and folders from the working_dir
    except in ignored_dirs and returns a list of
    media file paths: pictures and videos the script can
    generate a proxy for
    """
    files = []
    FILE_EXTENSIONS = list(Video.EXTS + Image.EXTS)
    for dirpath, dirnames, filenames in os.walk(working_dir):
        tail = os.path.split(dirpath)[1]
        if tail in ignored_dirs:
            dirnames[:] = []
            continue

        for f in filenames:
            file_path = os.path.join(dirpath, f)
            extension = os.path.splitext(file_path)[1]
            if extension.lower() in FILE_EXTENSIONS:
                files.append(os.path.join(dirpath, f))
    return files

if __name__ == '__main__':
    """
    The actual script:
    1) get the working dir from args
    2) scan dir for media objects and add them
    3) print results of scan
    4) create proxy
        - create path
        - issue ffmpeg command and print progress
    """
    working_dir = parse_cmd_args()
    

    media_file_paths = get_media_file_paths(working_dir)
    media_objects = []

    for path in media_file_paths:
        if Video.isVideo(path):
            media_objects.append(Video(path))
        elif Image.isImage(path):
            media_objects.append(Image(path))


    total = len(media_objects)
    print('found %d file(s) to convert' % total)
    for media in media_objects:
        print('~~ %s' % media.path_orig)

    count = 1
    for media in media_objects:
        print()
        print("%d/%d :: %s" % (count, total, media.path_orig))
        media.create_proxy_path()
        media.create_proxy_file()
        count += 1

