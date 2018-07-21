#!/usr/bin/python
"""
Renders videos edited in Blender 3d's Video Sequence Editor using multiple CPU cores
Original script by Justin Warren: https://github.com/sciactive/pulverize/blob/master/pulverize.py
Modified by sudopluto (Pranav Sharma) and gdquest (Nathan Lovato)
Under GPL license
"""
import argparse
import os
import multiprocessing
import signal
import subprocess
import math
import logging

# https://github.com/mikeycal/the-video-editors-render-script-for-blender#configuring-the-script
# there seems no easy way to grab the ram usage in a mulitplatform way
# without writing platform dependent code, or by using a python module

# Most popluar config is 4 cores, 8 GB ram, this is the default for the script
# https://store.steampowered.com/hwsurvey/
CPUS_COUNT = min(int(multiprocessing.cpu_count() / 2), 6)
PATH_TO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
log = logging.getLogger()


def get_project_info(blendfile):
    """
    opens blender, has blender write out the start and end frames of the scene,
    generates the render path, and returns the trio as a tuple
    """
    get_info_blender_script = os.path.join(PATH_TO_SCRIPT, "blender_scripts/get_project_info.py")
    get_blender_info_cmd = ["blender", "-b", blendfile, "-P", get_info_blender_script, "-Y"]
    process = subprocess.Popen(
        get_blender_info_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True)

    frame_start, frame_end = 0, 0
    render_path = os.path.join(os.path.split(blendfile)[0], "render")

    for line in process.stdout:
        if line.startswith("START"):
            frame_start = int(line.split()[1])
        elif line.startswith("END"):
            frame_end = int(line.split()[1])
    return (frame_start, frame_end, render_path)


def generate_render_chunk_commands(render_settings, frame_start, frame_end, render_path):
    """
    Returns a list of cmds to run in order to generate chunks
    """
    def generate_blender_render_command(render_settings, start_frame, end_frame, render_path):
        """
        Returns a command as a list of strings to spawn a chunk render process
        """
        blendfile, workers = render_settings
        chunk_path = os.path.join(render_path, "render_parts", "render_chunk_")
        render_video_only_script = os.path.join(PATH_TO_SCRIPT, "blender_scripts/render_video_only.py")
        return ["blender", "-b", blendfile, "-s",
                str(start_frame), "-e",
                str(end_frame), "-o", chunk_path, "-a",
                "-P", render_video_only_script, "-Y"]

    total_frames = frame_end - frame_start
    blendfile, workers = render_settings
    chunk_length = int(math.floor(total_frames / workers))
    log.debug("Project length in frames: {!s}".format(total_frames))
    log.debug("Frame count per worker: {!s}".format(chunk_length))

    render_chunk_commands = []
    for i in range(workers):
        w_start_frame = frame_start + (i * chunk_length)
        if i == workers - 1:
            w_end_frame = frame_end
        else:
            w_end_frame = w_start_frame + chunk_length - 1
        render_command = generate_blender_render_command(render_settings, w_start_frame, w_end_frame, render_path)
        log.debug("Worker {!s} frame range: {!s} to {!s}".format(i, w_start_frame, w_end_frame))
        render_chunk_commands.append(render_command)

    # DEBUG MESSAGE
    commands_as_string = ""
    for c in render_chunk_commands:
        command = " ".join(c)
        commands_as_string += command + "\n"
    log.debug("Commands:\n%s" % commands_as_string)
    return render_chunk_commands


def render_multiprocess(commands_list):
    """
    Manages the chunk rendering processes via a pool
    many thanks to this blog post:
    https://rsmith.home.xs4all.nl/programming/parallel-execution-with-python.html
    """
    # def process_kbd_interrupt_signal():
    #     signal.signal(signal.SIGINT, signal.SIG_IGN)

    assert commands_list
    pool = multiprocessing.Pool(len(commands_list))
    try:
        pool.map(render_chunk, commands_list)
        pool.close()
    except KeyboardInterrupt:
        print("KeyboardInterrupt: terminating process")
        pool.terminate()
    except Exception as e:
        pool.terminate()
    finally:
        pool.join()


def render_chunk(command):
    """
    Spawns a subprocess to render one chunk of the video
    """
    subprocess.check_output(command, stderr=subprocess.STDOUT)


def generate_render_mixdown_command(render_settings, render_path):
    """
    renders the audio on a single thread, straight from blender
    """
    blendfile, workers = render_settings
    mixdown_script_path = os.path.join(PATH_TO_SCRIPT, "blender_scripts/render_mixdown.py")
    mixdown_cmd = ["blender", "-b", blendfile,
                   "-Y", "-P", mixdown_script_path]
    log.debug("Mixdown audio command: " + " ".join(mixdown_cmd))
    return mixdown_cmd


def generate_concatenate_command(render_parts_path, chunk_list_path):
    """
    Generates and returns an FFMPEG command to call as a subprocess
    """
    ext = ""
    for f in os.listdir(render_parts_path):
        if f.endswith(".txt") or f.endswith(".flac"):
            continue
        ext = os.path.splitext(f)[1]
        break
    concat_path = os.path.join(render_parts_path, "video_concat" + ext)

    concat_cmd = ["ffmpeg", "-stats", "-f", "concat", "-safe", "-0", "-i",
                  chunk_list_path, "-c", "copy", "-y", concat_path]
    log.debug("FFMPEG concatenate command: " + " ".join(concat_cmd))
    return concat_cmd


def get_chunks_files_as_list(chunk_list_path):
    """
    Create a text file with a list of video chunks to concatenate with FFMPEG
    Returns the path to the newly created file
    """
    render_parts_path = os.path.split(chunk_list_path)[0]

    chunk_list = []
    for file in os.listdir(render_parts_path):
        if file.startswith("render_chunk_"):
            chunk_list.append(file)
    chunk_list = sorted(chunk_list)
    log.debug("Render chunks:\n%s" % chunk_list)
    return chunk_list


def create_chunks_list_file(file_path, _file_list):
    with open(file_path, "w") as chunk_list_file:
        lines = []
        for chunk in chunk_file_list:
            chunk_abspath = os.path.join(render_parts_path, chunk)
            log.debug(chunk_abspath)
            lines.append("file \'{!s}\'".format(chunk_abspath) + "\n")
        chunk_list_file.writelines(lines)


def call(command):
    """
    Call a command with Popen and wait for it to finish
    """
    subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True).wait()


def generate_join_parts_command(render_path, concat_video_file_path):
    """
    Calls ffmpeg to join the video and the audio in order to create the final
    render
    """
    mixdown_path = os.path.join(render_path, "render_parts", "mixdown.flac")
    ext = os.path.splitext(concat_video_file_path)[1]
    return [
        "ffmpeg", "-stats", "-i", concat_video_file_path, "-i", mixdown_path,
        "-map", "0:v:0", "-c:v", "copy",
        "-map", "1:a:0", "-c:a", "aac", "-b:a", "192k",
        "-y", os.path.join(render_path, "render" + ext)
    ]


def parse_arguments():
    ap = argparse.ArgumentParser(
        description="Multi-process Blender VSE rendering",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, )
    ap.add_argument(
        "-w",
        "--workers",
        type=int,
        default=CPUS_COUNT,
        help="Number of workers in the pool.")
    ap.add_argument(
        '--dry-run',
        action='store_true',
        default=False,
        help="Run the script without actual rendering or creating files and folders. For debugging purposes")
    ap.add_argument(
        '-d',
        '--debug',
        action='store_true',
        default=False,
        help="Print debug log messages to the console")
    ap.add_argument(
        '--concatenate-only',
        action='store_true',
        default=False,
        help="Only concatenate the video chunks and merge the video and audio mixdown")
    ap.add_argument("blendfile", help="Blender project file to render.")

    args = ap.parse_args()
    args.blendfile = os.path.abspath(args.blendfile)
    return args


# SCRIPT
if __name__ == "__main__":
    args = parse_arguments()
    render_settings = (args.blendfile, args.workers)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    print("~~ probing blendfile for project info... ")
    frame_start, frame_end, render_path = get_project_info(args.blendfile)
    print("Done!\n")

    render_parts_path = os.path.join(render_path, "render_parts")
    if not os.path.exists(render_parts_path):
        os.makedirs(os.path.join(render_path, "render_parts"))

    render_chunk_commands = generate_render_chunk_commands(render_settings, frame_start, frame_end, render_path)
    mixdown_command = generate_render_mixdown_command(render_settings, render_path)

    if not (args.dry_run or args.concatenate_only):
        print("~~ rendering video and audio")
        render_multiprocess(render_chunk_commands)
        print("Rendering video chunks done!")

        call(mixdown_command)
        print("Done!\n")

    chunks_file_path = os.path.join(render_parts_path, "chunks_list.txt")

    concatenate_command = generate_concatenate_command(render_parts_path, chunks_file_path)
    log.debug(" ".join(concatenate_command))
    concat_video_file_path = concatenate_command[-1]
    join_audio_video_command = generate_join_parts_command(render_path, concat_video_file_path)
    log.debug(" ".join(join_audio_video_command))

    chunk_file_list = get_chunks_files_as_list(chunks_file_path)
    log.debug("Chunks file path: %s" % chunks_file_path)
    create_chunks_list_file(chunks_file_path, chunk_file_list)

    if not chunk_file_list:
        log.warn("No render chunks found, cannot concatenate the video.")
    elif not args.dry_run:
        print("~~ now joining parts to make final render... ")
        call(concatenate_command)
        subprocess.call(join_audio_video_command)
        print("Done!\n")

    os.remove(chunks_file_path)
