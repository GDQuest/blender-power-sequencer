import bpy
import os

# Dimension Preset -
# TODO: move presets to external files!
# Then use a single function to call the right preset script, i.e. presets/youtube.py
def set_render_dimensions(x = None, y = None, resolution_percentage = 100, pixel_ratio_x = 1,
                          pixel_ratio_y = 1, fps = 24, fps_base = 1):
    """Sets the render parameters: dimensions, pixel ratio, resolution percentage, and framerate"""

    render = bpy.context.scene.render

    if x != None:
        render.resolution_x = x
    if y != None:
        render.resolution_y = y
    render.resolution_percentage = resolution_percentage
    render.pixel_aspect_x = pixel_ratio_x
    render.pixel_aspect_y = pixel_ratio_y
    render.fps = fps
    render.fps_base = fps_base
    return True


def set_render_encoding(preset):
    """"Sets the render format and ffmpeg encoding settings"""

    render = bpy.context.scene.render
    ffmpeg = render.ffmpeg

    if preset == 'youtube':
        render.image_settings.file_format = 'H264'
        ffmpeg.format = 'MPEG4'
        ffmpeg.codec = 'H264'
        ffmpeg.gopsize = 18
        ffmpeg.video_bitrate = 9000
        ffmpeg.maxrate = 9000
        ffmpeg.minrate = 0
        ffmpeg.buffersize = 224 * 8
        ffmpeg.packetsize = 2048
        ffmpeg.muxrate = 10080000
        ffmpeg.audio_codec = 'AAC'
        ffmpeg.audio_bitrate = 192
        return True
    else:
        print("The preset you asked for doesn't exist")
        return False


# 1 click render video with correct encoding params for Youtube
# Auto sets the file name
# TODO: Add optional system to generate proxies/lower res files with FFMPEG (in proxy_management.py)
# TODO: Give ability to render lower res videos using the proxies generated with FFMPEG
#       The script would automatically switch to the proxy for rendering? Then other operator/function to switch back to full res proxies
class RenderVideoWeb(bpy.types.Operator):
    bl_idname = "gdquest_vse.render_video_web"
    bl_label = "Render for Youtube"
    bl_description = "Quickly export the video next to your blend file for Youtube in HD"
    bl_options = {"REGISTER"}

    # Properties
    # encoding = bpy.props.StringProperty("youtube")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        set_render_dimensions(1920, 1080, 100, 1, 1, 24, 1)
        set_render_encoding('youtube')

        # Set the export filepath
        if bpy.data.is_saved:
            filename = bpy.path.basename(bpy.data.filepath)
            filename = os.path.splitext(filename)[0]
            filename += '.mp4'
            bpy.context.scene.render.filepath = "//" + filename if filename != "" else "Video.mp4"
            bpy.ops.render.render({'dict': "override"},
                                  'INVOKE_DEFAULT',
                                  animation=True)
            pass
        return {"FINISHED"}
