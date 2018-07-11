import bpy

for strip in bpy.context.scene.sequence_editor.sequences_all:
    if strip.type != "SOUND":
        strip.mute = True

bpy.ops.sound.mixdown(filepath="//render/render_parts/mixdown.flac", check_existing=False, relative_path=True, container="FLAC", codec="FLAC")
