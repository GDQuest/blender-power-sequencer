# Power Sequencer 1.1

*Huge thanks to all the contributors who made this release possible: @doakey3 and @sudopluto, @razcore-art, @jooert, and @Blezyn, who recently joined the adventure 😊. Thanks to them this new version brings many new features and improvements to the add-on!*

## Free tutorials

**Two new tutorials** came out to complement the project. They are about Python programming, to help more people create their own tools and contribute to existing add-ons:

- [Learn to Code Blender Features in Python: Add-On Programming Tutorial](https://www.youtube.com/watch?v=1_Jo9NShkP8)
- [Auto-Completion for Blender Python in Any Code Editor](https://www.youtube.com/watch?v=IQgLBnPO2uo)

## 🎥🕺 New features

- **Multithreaded rendering** with BPSRender: use this command line tool to leverage all your CPU cores! Works on all platforms and available as a stand-alone program. ⚠ Only tested on Ubuntu and Windows 10! *Known issues: on Windows, you will sometimes need to close Blender instances manually with the task manager if you interrupt the render.*

- **Unspeed**: remove a speed effect from a video sequence
- **Clear fades**: remove fade animation cleanly on selected sequences
- **Deselect strips** to the left or right of the time cursor
- **Swap two strips**: works across channels and not just to the left or the right of the selected strip, unlike Blender's built-in tool
- **Markers as time codes**: write a list of timecodes followed by the markers' names to create quick links in your YouTube video description or comments
- **Match strips to markers**: snap selected strips to markers that have a similar name

## ✅ Improvements

*Existing features got some love as well!*

- **Multithreaded proxies** now shows a percentage-based progress for each video being rendered
- **Multithreaded proxies**: supports calling presets from the command line. More work planned for version 1.2
- Many small improvements happened to exsting features, e.g. to automatically select strip near the mouse cursor if nothing is selected.

## 🤕 Fixes

**Restored the missing interface** code so you can call the contextual Power Sequencer menu again, nd find the power sequencer tab i the and menu. we need help to design the UI: we have a developer who wants to work on it, but we need a UX designer to guide him!

Reply to [this issue](https://github.com/GDquest/Blender-power-sequencer/issues/90) and [that issue](https://github.com/GDquest/Blender-power-sequencer/issues/89) if you want to help us wit it 😄

## ⚠ Experimental

- **Auto align audio and video**: this tool for tech-savy people, currently not available in blender
- **Batch transcode videos**: transcode selected videos to the same frame rate from blender! Uses FFMPEG. More work planned for version 1.2
- **Trim in and and out points**: trim the left or the right of the strip closest to the mouse, using the time cursor. No shortcut assigned by default: you'll have to create shortcut entries manually for `power_sequencer.trim_three_point_edit`
