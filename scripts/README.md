# Power Sequencer Utils

This folder contains extra tools to help develop the add-on or to help work with the add-on, but not as part of Blender.

## Blender Power Sequencer Proxy

BPSProxy is a standalone python program and a Python module to generate proxies in batch for Blender, from your terminal.

More information: [BPSProxy repository](https://github.com/GDQuest/blender-proxies-generator)


## Blender Power Sequencer Render

BPSRender is a python program to speed up the rendering of Blender Sequencer projects. It spawns several Blender processes in the background in parallel and joins the resulting video clips.

It is a temporary workaround for the performance limitations of the sequencer, that uses a single thread for most of the rendering work.

More information: [BPSRender repository](https://github.com/GDQuest/blender-sequencer-multithreaded-render)
