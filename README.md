<h1 align="center">
  Blender Power Sequencer</br>
  <small>The Free add-on for content creators</small>
</h1>

<p align='center'>
  <img src="https://i.imgur.com/6tVdzBQ.jpg" alt="Power Sequencer logo, with the add-on's name and strips cut in two" />
</p>

Blender's video sequencer has a lot of potential, but it lacks essential tools for content creators to edit videos efficiently.

I made [hundreds of tutorials](http://youtube.com/c/gdquest) over the years. After working with popular yet unstable professional programs like Vegas and Resolve, I now **work exclusively with Blender**. It does have some limitations, but it's the most stable and versatile tool you'll find out there.

I built Power Sequencer to help us edit videos as fast as possible. The add-on is getting better month after month, and it's yours for Free.

## Features

<p align='center'>
  <img src="https://i.imgur.com/ZWu6TzT.gif" alt="Power Sequencer in action. Showing import, mouse-based tools and export" />
</p>

1. **Instant import**: finds and imports all new videos, images and sound files in your project folder
1. Render HD videos for Youtube, Twitter and Facebook in one keyboard shortcuts: Power Sequencer sets all the rendering parameters for you
1. **Cut, trim and edit faster than ever** in Blender with smart mouse-based tools
1. Instant fades and crossfades
1. Build **better proxies** with FFmpeg, using a Python script in the `utils/` folder
1. And much more

*To find all available tools, press <kbd>Spacebar</kbd> and search for 'PS.' (as in PowerSequencer).*

## Download the beta release

To install the add-on, head to the [latest releases](https://github.com/GDquest/Blender-power-sequencer/releases) and follow the instructions there.

It is stable already as I use it every single day for [ GDquest ](http://youtube.com/c/gdquest). It ships with a separate keymap file so the many custom shortcuts won't override your existing custom mappings.

## Give us a hand!

We're already working together with [ Davide Cristi ](https://github.com/davcri) to help more people create videos with Blender. This add-on is a living, open project, and we'd be glad to welcome new contributors! We need people to:

- Code new features
- Improve existing features
- Help solidify the code
- Write mini-tutorials on the [ docs repository ](https://github.com/GDquest/Blender-power-sequencer-docs/)

There's a convenient list of [Good first issues](https://github.com/GDquest/Blender-power-sequencer/labels/good%20first%20issue) to help you get started. I'm also available to help you navigate the code or if you have questions about the project.

## Learn video editing with Power Sequencer and Blender

The docs are in progress. Until the dedicated website is ready, you can find them on the [ power-sequencer-docs repository ](https://github.com/GDquest/Blender-power-sequencer-docs/). There's also a growing list of [ Free video tutorials ](https://www.youtube.com/playlist?list=PLhqJJNjsQ7KFjp88Cu57Zb9_wFt7nlkEI) on Youtube (*14 videos at the time of writing*).

These are not classical docs: on top of Power Sequencer's features, we're looking to help you improve your understanding of Blender's video editing tools too!

**Docs Contents**

- [Import local footage](#import-local-footage)
- [Cut and Trim with the Mouse](#cut-and-trim-with-the-mouse)
    - [Cut strips](#cut-strips)
    - [Trim strips](#trim-strips)
    - [Toggle Mute strips](#toggle-mute-strips)
- [Crossfades](#crossfades)
- [Fade-in and fade-out](#fade-in-and-fade-out)
- [Render videos for the web](#render-videos-for-the-web)


## Import local footage ##

Imports all images, videos and audios from folders named respectively: `img`, `video` and `audio`.

![Import Local Footage](https://imgur.com/9cZEAny.gif)

1. Create folders named `img`, `video` and `audio` inside your Blender project folder (where your *.blend* file is)
2. Put your source images, videos and audio files in the corresponding folders
3. In Blender, press <kbd>Ctrl</kbd><kbd>Shift</kbd><kbd>I</kbd> (shortcut for `PS.Import local footage` operator)

*You must save your Blender project before you use this feature.*

## Cut and Trim with the Mouse ##

You can cut and trim strips with mouse clicks using the add-on.

The cut and trim tool has two main modes:

1. The **smart** mode is the default. If you click on a strip, it will only cut this strip. If you click on a gap between two blocks of strips, it will remove the gap. And if you click above the strips, it will cut every strip in the sequencer on that frame.
2. The **time cursor** mode always cuts or trims all strips under the time cursor or on a given frame.

### Cut strips ###

#### Cut a single strip at a time ####

![Mouse cut a single strip by clicking on it](https://imgur.com/wTF5U3k.gif)

1. Place the mouse cursor over the strip to cut
2. Press <kbd>Ctrl</kbd><kbd>Action Mouse</kbd>

*By default <kbd>Action Mouse</kbd> is <kbd>Left Click</kbd> and <kbd>Select Mouse</kbd> corresponds to <kbd>Right Click</kbd>*

#### Cut all strips under the time cursor ####

![Mouse cut with the time cursor](https://imgur.com/NThKrQg.gif)

1. Place the mouse cursor on the sequencer, without hovering any strips
2. Press <kbd>Ctrl</kbd><kbd>Action Mouse</kbd>

To always cut in **time cursor** mode, press <kbd>Ctrl</kbd><kbd>Shift</kbd><kbd>Action Mouse</kbd> instead.

You can also use this operator to cut gaps between strips. Hover a gap and press <kbd>Ctrl</kbd><kbd>Action Mouse</kbd> to remove it.

### Trim strips ###

#### Trim a single strip at a time ####

![Mouse trim](https://imgur.com/kfo7DhW.gif)

1. Place the mouse cursor over the strip that you want to cut
2. Press <kbd>Ctrl</kbd><kbd>Select Mouse</kbd>

#### Trim all strips ####

![Mouse trim with the time cursor and auto remove gaps](https://imgur.com/q3LIH4v.gif)

1. Place the mouse cursor on the sequencer, without hovering on any strips
2. Press <kbd>Ctrl</kbd><kbd>Select Mouse</kbd>

To always trim in **time cursor** mode, press <kbd>Ctrl</kbd><kbd>Shift</kbd><kbd>Action Mouse</kbd> instead.

---

Keyobard shortcuts are the quickest way to activate these operations, but they also can be accessed by the [operator search pop-up menu](https://docs.blender.org/manual/en/dev/interface/controls/templates/operator_search.html).

### Trim to the closest cuts and cut the gap ###

Auto-trim a strip to the closest surrounding cuts, leave some margin and remove the newly formed gap.

> Placeholder for the video demo

1. Press <kbd>Shift</kbd><kbd>Alt</kbd><kbd>Action Mouse</kbd> where you want to cut on the sequencer. You don't need to click on a strip in particular.

*Use this tool when you've edited some audio out and you're left with extra footage you want to remove. It finds the closest cuts around the time cursor, cuts and trims the strips it overlaps up to the surrounding cuts and it leaves a few frames on either side.*

### Toggle Mute strips ###

Press <kbd>Alt</kbd><kbd>Action Mouse</kbd> on a strip to toggle it muted with the mouse.

This leaves the strip in the channel so when you trim audio or footage around it, the muted strip will block the rest of the edits.

It's useful when you're editing audio separately from the video which is common with tutorials and other screencasts.

*It also works during playback and leaves the time cursor running.*


### Techniques ###

You can resize mute strips to add space between 2 other strips. Grab the mute sequence's handle, and keep the alt key down to ripple the edit.

Want to shorten it instead? Mouse trim it with Ctrl Right Click, and let Power Sequencer remove the gap.

#### Add a muted sound strip to leave some space in your edits ####

Select and drag the left handle of the sequence to the right of a cut to extend it while you keep the <kbd>Alt</kbd> key down. This will ripple the edit, or push the sequence to the right.

<kbd>Ctrl</kbd><kbd>Action Mouse</kbd> to cut the extra audio or footage, and <kbd>Alt</kbd><kbd>Action Mouse</kbd> the new small sound sequence. You now have a block that will leave some time between the 2 sequences, even when you remove all gaps!

#### Quickly cut and mute bad sounds with the mouse ####

It's common to have pops, or little coughs in the audio. Often the speaker is so fast you don't want to trim them. Instead, you'd rather keep the strip around as a spacer but you may want to mute them.

1. <kbd>Ctrl</kbd><kbd>Action Mouse</kbd> before and after the incriminated sound on the waveform to cut a new strip.
2. <kbd>Alt</kbd><kbd>Action Mouse</kbd> on the new sound strip to mute it.

## Crossfades ##

Crossfades or dissolves are smooth transitions from one video or image strip to another. To achieve a crossfade in Blender you add a cross or gamma cross effect strip that stacks on top of two video or image strips.

### Add a crossfade ###

![Add crossfade](https://i.imgur.com/5iHA6fv.gif)

1. Select one strip to fade from
1. Press <kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>c</kbd> (*shortcut for `PS.Add Crossfade` operator*)

*Power Sequencer finds the closest strip to fade to for you. It looks from strips that start after the active selected strip end frame. If the strip already overlaps with your selection Power Sequencer will ignore it and move to the next one in the editor. It will also first look for strips in the same channel or neighboring channels.*

### Slide a crossfade ###

![Edit crossfade](https://imgur.com/rQJi1PH.gif)

1. Select the Gamma Cross effect strip
1. Press <kbd>Alt</kbd><kbd>c</kbd> (*shortcut for `PS.Edit crossfade` operator*)

*This tool finds and selects the handles of the effect's input strips. Then it fires the grab mode. It's a shortcut to move a gamma cross effect faster.*

## Fade-in and fade-out ##

Fade-in and fade-out are gradual opacity transitions.

### Add fade-in and fade-out ###

![Fade in and out](https://imgur.com/VMLv0dW.gif)

1. Select one or more strips
2. Press <kbd>f</kbd>

### Add fade-in ###

![Fade in only](https://imgur.com/faz3jdV.gif)

1. Select one or more strips
2. Press <kbd>Ctrl</kbd><kbd>f</kbd> (*shortcut for operator: `PS.Fade strips`*)

### Add fade-out ###

![Fade out only](https://imgur.com/D97KrFe.gif)

1. Select one or more strips
2. Press <kbd>Alt</kbd><kbd>f</kbd>

### General fade tips ###

When you apply a fade, its transition function will appear in the [Blender graph editor](https://docs.blender.org/manual/en/dev/editors/graph_editor/introduction.html). You can edit individual key frames to adjust the fade as you like.

Try to add fades at the very end of your video editing process otherwise you can encounter caveats that can create slowdowns; if you want to know more, see the documentation video ["Power Sequencer: Fade in, fade out"](https://youtu.be/7v2WLP-gqJQ?t=2m16s).

#### Add a fade with operator ####

By default `PS.Fade strips` will use the *Fade-in*, but you can also use other types with these steps:

1. Select one or more strips
2. Use the `PS.Fade strips operator` (<kbd>Ctrl</kbd><kbd>f</kbd>)
3. Press <kbd>F6</kbd> to access operator properties
4. Change `Fade Type`

### Techniques ###

#### Dim a strip ####

1. Add a color strip above on che channel above the strip you want to dim
    1. Press <kbd>Shift</kbd><kbd>a</kbd>
    2. Select *Effect Strip -> Color*
2. Select the color strip
3. Set blend to alpha over
4. Adjust the length of the color strip
5. Adjust the opacity (this value is used as the max opacity of the strip, so pick a value < 1.0)
6. Press <kbd>f</kbd>


## Render videos for the web ##

Renders a video using the preset options specified in the preferences.

### Render the video ###

![Render for the web](https://imgur.com/gqLl4Qh.gif)

1. Place the mouse cursor over the *Video Sequencer Editor*
2. Press <kbd>Alt</kbd><kbd>F12</kbd> (shortcut for `PS.Render video for the web` operator)

Blender uses only one CPU core for the rendering. This means that
it's possible to do other things during the rendering: you can also open another Blender
instance and start editing a new video, withouth major slowdowns.

### Change rendering preferences ###

1. Press <kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>U</kbd> to access *User Preferences*
2. Select the *Input tab*
3. Search for `PS.Render video for the web`
4. Click the arrow to expand details of the keymap

You will see something like:

![Rendering videos preferences](img/rendering-videos-preferences-highlight.png)

#### Preset ####

The preset contains rendering options such as resolution, container, and codecs.

At the moment there are only two presets available.

| Preset      | Resolution | Container | Video codec | Audio codec |
| -           | -          | -         | -           | -           |
| **youtube** | 1080p      | mp4       | h264        | AAC         |
| **twitter** | 720p       | mp4       | h264        | AAC         |


#### Filename ####

Filename of the rendered video. It can be one of:
- **Blender file**: the name of the main *.blend* file
- **Current scene**: the name of the current [Blender scene](https://docs.blender.org/manual/en/dev/data_system/scenes/introduction.html)
- **Folder**: the name of the folder containing the main *.blend* file

#### Auto render ####

If checked (it's the default setting), the `PS.Render video for the web` operator will automatically start the rendering.

If unchecked, it will only update rendering settings, but it will not start rendering: to start the render,
you will need to click on the *Animation* button in the *Properties Editor*.

## Other add-ons

Here are other recommended add-ons for a better editing workflow:

1. [VSE transform tools](https://github.com/kgeogeo/VSE_Transform_Tools): Move and animate transform effects visually, on the image preview area. The addon auto-registers shortcuts, especially the <kbd>T</kbd> key, to add a Transform effect to selected sequences.
2. [Easy logging](http://www.easy-logging.net/): Adds tools to derush and tag footage.

## Credits

- [davcri](https://github.com/davcri)
- [ Nathan Lovato ](https://twitter.com/NathanGDquest)
