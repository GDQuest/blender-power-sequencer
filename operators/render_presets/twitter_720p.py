import bpy

# Resolution
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.pixel_aspect_x = 1
bpy.context.scene.render.pixel_aspect_y = 1

# FFMPEG
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = "MPEG4"
bpy.context.scene.render.ffmpeg.codec = "H264"

bpy.context.scene.render.ffmpeg.constant_rate_factor = 'HIGH'
bpy.context.scene.render.ffmpeg.ffmpeg_preset = 'MEDIUM'


is_ntsc = (bpy.context.scene.render.fps != 25)
if is_ntsc:
    bpy.context.scene.render.ffmpeg.gopsize = 18
else:
    bpy.context.scene.render.ffmpeg.gopsize = 15
bpy.context.scene.render.ffmpeg.use_max_b_frames = False

bpy.context.scene.render.ffmpeg.video_bitrate = 4000
bpy.context.scene.render.ffmpeg.maxrate = 4000
bpy.context.scene.render.ffmpeg.minrate = 0
bpy.context.scene.render.ffmpeg.buffersize = 224 * 8
bpy.context.scene.render.ffmpeg.packetsize = 2048
bpy.context.scene.render.ffmpeg.muxrate = 10080000