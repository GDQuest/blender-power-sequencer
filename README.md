# Power Sequencer: free Blender addon for content creators
Blender's video sequencer has a lot of potential, but it lacks essential tools for content creators to edit fast. I produced [hundreds of tutorials](http://youtube.com/c/gdquest) since 2015, and work exclusively with Blender. Here are the tools I built to edit tutorials faster.

## Heavy Work in Progress

The operators work, but the add-on is not documented yet. You'll have to find and assign the operators to shortcuts by yourself, or use [this keymap](https://gist.github.com/NathanLovato/84b3a8529e5757875c8e97f4d7b424f4).

## Other add-ons

Here are other recommended add-ons for a better editing workflow:

1. [VSE transform tools](https://github.com/kgeogeo/VSE_Transform_Tools): Move and animate transform effects visually, on the image preview area
2. [Easy logging](http://www.easy-logging.net/): Adds tools to derush and tag footage


# Available tools

## Mouse-based editing tools

### Cut and Trim

Cut or trim strips sitting right under the mouse cursor, under the time cursor, or both with the "smart mode", active by default. 

## Import and export

### Import local footage

Import videos, audio and pictures sitting around the .blend project file with a single keystroke! For now, you must put the files in subfolders named:

1. audio for the audio files (.wav, etc.)
2. img for the pictures (.png, etc.)
3. video for the video clips (.mp4, .mkv, etc.)

The function will find all the valid audio, image and video files in your project's subfolders and import them to the sequencer. The next version will allow you to [use any folder structure](https://github.com/GDquest/GDquest-VSE/issues/2) you'd like.

### Render video for the web

Automatically set the project's resolution, encoding parameters, name the exported video file and render the project. By default, it exports a full HD mp4 file optimized for Youtube next to the .blend file, named after the project's directory.

E.g. if your blend file is in "my-video/project.blend", it will export the video as "my-video.mp4".