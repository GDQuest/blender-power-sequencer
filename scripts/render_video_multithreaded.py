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

# https://github.com/mikeycal/the-video-editors-render-script-for-blender#configuring-the-script
# there seems no easy way to grab the ram usage in a mulitplatform way
# without writing platform dependent code, or by using a python module

# https://store.steampowered.com/hwsurvey/
# most popluar config is 4 cores, 8 GB ram, so lets take that as our default
# with that being our default, this constant makes sense
CPUS_COUNT = min(int(multiprocessing.cpu_count() / 2), 6)
UTIL_SCRIPT = "./render_video_multithreaded_script.py"


def get_project_data(args):
    """
    opens blender, has blender write out scence start, scence end, and render
    path

    todo:
    - default render path? (wath happens if its not set)
    - avoid using a seperate file? (write file from string, then delete?)
    """
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

    Right now the blender instances are local to here
    If we want a graceful shutdown, we should try to 
    return the instances, instead of running them directly from here
    """
    total_frames = frame_end - frame_start
    chunk_frames = int(math.floor(total_frames / args.workers))

    processes = []
    # Figure out the frame ranges for each worker.
    # The last worker will need to render a few extra
    # frames if the total number of frames doesn't Divide
    # neatly, but this is usually a relatively small number
    # of extra frames, so we don't need to create an entirely
    # new worker to work on it.
    for i in range(args.workers):
        w_start_frame = frame_start + (i * chunk_frames)
        if i == args.workers - 1:
            # Last worker takes up extra frames
            w_end_frame = frame_end
        else:
            w_end_frame = w_start_frame + chunk_frames - 1

        # Set a worker to work on this frame range
        p = multiprocessing.Process(
            target=render_proc,
            args=(args, w_start_frame, w_end_frame, render_directory))
        processes.append(p)
        p.start()

    # wait for results
    for i, p in enumerate(processes):
        p.join()


def render_proc(args, start_frame, end_frame, render_directory):
    """
    Render a chunk of the blender file.

    This part is failing on my linux machine with an invalid path,
    needs some cleaning up

    Do we need to keep the dry run?
    """
    # TODO: clean up
    outfilepath = os.path.join("//", render_directory, "render_chunk_#######")
    params = [
        'blender', '-b', args.blendfile, '-s',
        '%s' % start_frame, '-e',
        '%s' % end_frame, '-o', outfilepath, '-a'
    ]
    if not args.dry_run:
        proc = subprocess.Popen(
            params, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdoutdata, stderrdata = proc.communicate()


def join_chunks(args, render_directory):
    """
    Concatenate the video chunks together with ffmpeg

    I wonder if reading in from the current directory is needed.
    We could try to keep the chunk files in memory, or add them to the list
    When the jobs complete
    """
    chunk_files = sorted(f for f in os.listdir(render_directory) if "render_chunk" in f)

    list_file = os.path.join(render_directory, 'render_chunks_list.txt')

    with open(list_file, 'w') as fp:
        fp.write('\n'.join(["file %s" % x for x in chunk_files]))
    filebase = os.path.splitext(args.blendfile)[0]
    print(args.blendfile)
    # TODO: get container/extension from before/elsewhere in the script
    extension = os.path.splitext(os.path.basename(chunk_files[0]))[1]
    output_path = os.path.join(filebase, "output" + extension)
    command = [
        'ffmpeg', '-stats', '-f', 'concat', '-safe', '0', '-i', list_file,
        '-c', 'copy', output_path
    ]
    sys.exit()
    if args.dry_run:
        return
    subprocess.check_output(command)

if __name__ == '__main__':
    """
    Again, not sure if a dry run is really needed
    Should probably bring out arg parsing into its own function
    
    """
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
