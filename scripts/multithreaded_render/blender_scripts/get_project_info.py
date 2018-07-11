import bpy

scene = bpy.context.scene
print("START %d" % (scene.frame_start))
print("END %d" % (scene.frame_end))
