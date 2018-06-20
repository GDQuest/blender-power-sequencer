#!/usr/bin/python
"""
Renders videos edited in Blender 3d's Video Sequence Editor using multiple CPU cores
Original script by Justin Warren: https://github.com/sciactive/pulverize/blob/master/pulverize.py
Under GPL license
"""

import argparse
import os
import multiprocessing
import subprocess
import math
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("render_multithreaded")

CPUS_COUNT = min(int(multiprocessing.cpu_count() / 2), 6)
UTIL_SCRIPT = "./render_video_multithreaded_script.py"

def get_project_data(args):
    realpath = os.path.dirname(os.path.realpath(__file__))
    utilfile = os.path.join(realpath, UTIL_SCRIPT)
    command = ['blender', '-b', args.blendfile, '-P', utilfile]
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True)

    frame_start, frame_end = 0, 0
    render_path = ""
    for line in process.stdout:
        if line.startswith("START"):
            frame_start = int(line.split()[1])
        elif line.startswith("END"):
            frame_end = int(line.split()[1])
        elif line.startswith("RENDERPATH"):
            render_path = line.split()[1]

    return (frame_start, frame_end, render_path)


def render_chunks(args, frame_start, frame_end, render_directory):
    """
    Divide render into even sized chunks
    """
    log.info("Render frames from %s to %s", frame_start, frame_end)
    total_frames = frame_end - frame_start
    log.debug("total frames: %s", total_frames)
    chunk_frames = int(math.floor(total_frames / args.workers))
    log.debug("chunk_frames: %s", chunk_frames)

    processes = []
    # Figure out the frame ranges for each worker.
    # The last worker will need to render a few extra
    # frames if the total number of frames doesn't Divide
    # neatly, but this is usually a relatively small number
    # of extra frames, so we don't need to create an entirely
    # new worker to work on it.
    for i in range(args.workers):
        log.debug("Setting params for worker %d", i)
        w_start_frame = frame_start + (i * chunk_frames)
        if i == args.workers - 1:
            # Last worker takes up extra frames
            w_end_frame = frame_end
        else:
            w_end_frame = w_start_frame + chunk_frames - 1

        log.debug("worker %d rendering frames %d to %d", i, w_start_frame,
                  w_end_frame)

        # Set a worker to work on this frame range
        p = multiprocessing.Process(
            target=render_proc,
            args=(args, w_start_frame, w_end_frame, render_directory))
        processes.append(p)
        p.start()
        log.info("Started render process %d with pid %d", i, p.pid)

    # wait for results
    for i, p in enumerate(processes):
        log.debug("Waiting for proc %d", i)
        p.join()
    log.info("Render processes complete.")


def render_proc(args, start_frame, end_frame, render_directory):
    """
    Render a chunk of the blender file.
    """
    # TODO: clean up
    outfilepath = os.path.join("//", render_directory, "render_chunk_#######")
    params = [
        'blender', '-b', args.blendfile, '-s',
        '%s' % start_frame, '-e',
        '%s' % end_frame, '-o', outfilepath, '-a'
    ]
    log.debug("Render command: %s", params)
    if not args.dry_run:
        proc = subprocess.Popen(
            params, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdoutdata, stderrdata = proc.communicate()


def join_chunks(args, render_directory):
    """
    Concatenate the video chunks together with ffmpeg
    """
    chunk_files = sorted(f for f in os.listdir(render_directory) if "render_chunk" in f)
    log.debug("file list is: %s", chunk_files)

    list_file = os.path.join(render_directory, 'render_chunks_list.txt')

    with open(list_file, 'w') as fp:
        fp.write('\n'.join(["file %s" % x for x in chunk_files]))
    filebase = os.path.splitext(args.blendfile)[0]
    print(args.blendfile)
    # TODO: get container/extension from before/elsewhere in the script
    extension = os.path.splitext(os.path.basename(chunk_files[0]))[1]
    output_path = os.path.join(filebase, "output" + extension)
    log.debug(
        """
        Blend file base path: %s,
        extension %s
        output_path %s
        """, filebase, extension, output_path)
    log.info("Joining parts into: %s", output_path)
    command = [
        'ffmpeg', '-stats', '-f', 'concat', '-safe', '0', '-i', list_file,
        '-c', 'copy', output_path
    ]
    log.debug("ffmpeg command: %s", command)
    sys.exit()
    if args.dry_run:
        return
    subprocess.check_output(command)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        description="Multi-process Blender VSE rendering",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument(
        '-w',
        '--workers',
        type=int,
        default=CPUS_COUNT,
        help="Number of workers in the pool.")
    ap.add_argument(
        '--concat-only',
        action='store_true',
        default=False,
        help="Don't render new sections, just concat existing ones.")
    ap.add_argument(
        '--render-only',
        action='store_true',
        default=False,
        help="Render sections, but don't concat.")
    ap.add_argument(
        '--dry-run',
        action='store_true',
        default=False,
        help="Do everything but the complex, time-consuming subprocesses.")
    ap.add_argument('blendfile', help="Blender project file to render.")

    args = ap.parse_args()
    frame_start, frame_end, render_path = get_project_data(args)

    # TODO: needs testing and/or a cleaner solution
    render_directory = os.path.normpath(os.path.dirname(render_path))[1:]
    blender_project_folder = os.path.dirname(args.blendfile)
    render_directory_full_path = os.path.join(blender_project_folder, render_directory)

    if not args.concat_only:
        render_chunks(args, frame_start, frame_end, render_directory)
    if not args.render_only:
        join_chunks(args, render_directory_full_path)
