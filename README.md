# Power Sequencer: free Blender addon for content creators

Blender's video sequencer has a lot of potential, but it lacks essential tools for content creators to edit fast. I produced [hundreds of tutorials](http://youtube.com/c/gdquest) since 2015, and work exclusively with Blender. Here are the tools I built to edit tutorials faster.

## In alpha state

The addon works already, and I use it in production all the time. However, it's lacking documentation. To find the tools, press <kbd>Spacebar</kbd> and search for 'PS.' (_as in PowerSequencer_).

As there are many features, keymaps aren't automatically added. Version 1 will allow you to add keymaps from the preferences. In the meantime, you can use [this keymap file](https://github.com/GDquest/Blender-power-sequencer/blob/master/utils/power-vse-shortcuts.py). It's in the add-on's `/utils` folder.

## Docs and tutorials

The docs are currently on the [ GitHub Wiki ](https://github.com/GDquest/Blender-power-sequencer/wiki).

We also have a growing list of [ Free video tutorials ](https://www.youtube.com/playlist?list=PLhqJJNjsQ7KFjp88Cu57Zb9_wFt7nlkEI).

## Give us a hand!

We're already working together with Davide Cristi (https://github.com/davcri) to help more people create videos with Blender. This add-on is a living, open project, and we'd be glad to welcome new contributors! We need people to:

- Code new features
- Improve existing features
- Help solidify the code
- Write mini-tutorials on the [ docs repository ](https://github.com/GDquest/Blender-power-sequencer-docs/)

## Other add-ons

Here are other recommended add-ons for a better editing workflow:

1. [VSE transform tools](https://github.com/kgeogeo/VSE_Transform_Tools): Move and animate transform effects visually, on the image preview area. The addon auto-registers shortcuts, especially the <kbd>T</kbd> key, to add a Transform effect to selected sequences.
2. [Easy logging](http://www.easy-logging.net/): Adds tools to derush and tag footage.


# Features

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
