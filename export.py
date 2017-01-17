import bpy
from bpy.props import BoolProperty, EnumProperty


def set_render_settings(resolution=None, encoding=None):
    """Sets the render dimensions and encoding settings based on presets
       The presets are stored in the .functions.global_settings module"""

    if not resolution and encoding:
        return None

    rd = bpy.context.scene.render
    ff = bpy.context.scene.render.ffmpeg
    res, enc = resolution, encoding

    rd.resolution_x = res[0]
    rd.resolution_y = res[1]
    rd.resolution_percentage = res[2]
    rd.pixel_aspect_x = res[3]
    rd.pixel_aspect_y = res[4]
    rd.fps = res[5]
    rd.fps_base = res[6]

    rd.image_settings.file_format = enc[0]

    ff.format = enc[1]
    ff.codec = enc[2]
    ff.gopsize = enc[3]
    ff.video_bitrate = enc[4]
    ff.maxrate = 0
    ff.minrate = enc[6]
    ff.buffersize = enc[7]
    ff.packetsize = enc[8]
    ff.muxrate = enc[9]
    ff.audio_codec = enc[10]
    ff.audio_bitrate = enc[11]
    return True


# TODO: define resolution and framerate for the full video in one operator and then,
# in render for web, render for Youtube/twitter/facebook etc.
# based off that resolution
# That's a way to support people who make different types of videos / 30fps, etc.
# TODO: find way to set the right encoding using the preset enumProperty - dict?
# TODO: Remove proxy size
class RenderForWeb(bpy.types.Operator):
    bl_idname = "gdquest_vse.render_video"
    bl_label = "Render the video for the web"
    bl_description = "Pick a rendering preset and let Blender name and export \
        the video for you. Replaces strips with proxies if necessary."
    bl_options = {"REGISTER"}

    # from bpy.types import EnumProperty
    # TODO: Add menu to pick the rendering presets
    # TODO: Pass the rendering presets to set_render_dim using self.variables
    # TODO: add option to export to different folder
    # TODO: add file naming options

    # render_folder
    # file_name
    use_proxies = BoolProperty(
        name="Render at proxy size",
        description="Set strips to use proxies instead of full resolution clips and render",
        default=False)
    preset = EnumProperty(items=[
        ('youtube', 'youtube', 'Full HD mp4 with AAC audio, following recommendations from Youtube'),
        ('twitter', 'twitter', 'HD ready mp4 with high enough bitrate for Twitter and Facebook'),
        ('proxy', 'proxy', 'Fast rendering, uses proxies to render a low resolution video'),
        ('none', 'none', "Don't use any preset, but name the export and render using the current settings")],
        name='Preset',
        description='Preset to use ',
        default='youtube')
    use_preset = not preset == 'none'

    use_folder_name = BoolProperty(
        name="Use folder name",
        description="Use the folder to name the exported video, instead of the blend file",
        default=True)


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report({'WARNING'}, "Save your file first")
            return {'CANCELLED'}

        from .functions.global_settings import RENDER_SETTINGS as RS
        resolution = RS.RESOLUTION.PROXY if self.use_proxies else RS.RESOLUTION.HD_FULL
        encoding = RS.ENCODING.MP4_PROXY if self.use_proxies else RS.ENCODING.MP4_HIGH

        success = set_render_settings(resolution, encoding)
        if not success:
            self.report({'WARNING'}, "The rendering presets are not properly set. Cancelling operation")
            return {'CANCELLED'}

        # TODO: Replace with own proxy rendering system
        # if self.use_preset and 'velvet_revolver' in bpy.context.user_preferences.addons.keys():
        #     if self.use_proxies:
        #         bpy.ops.sequencer.proxy_editing_toproxy()
        #     else:
        #         bpy.ops.sequencer.proxy_editing_tofullres()

        from os.path import splitext, dirname
        path = bpy.data.filepath
        name = dirname(path).rsplit(sep="\\", maxsplit=1)[-1] \
            if self.use_folder_name else bpy.path.basename(path)

        if self.use_preset:
            name = "".join((splitext(name)[0], '_', self.preset, '.mp4'))
        else:
            name = "".join((splitext(name)[0], '.mp4'))

        bpy.context.scene.render.filepath = "//" + name if name else "Video.mp4"
        bpy.ops.render.render({'dict': "override"}, 'INVOKE_DEFAULT', animation=True)
        return {"FINISHED"}


# TODO: Write operator
class CopyStripsToNewScene(bpy.types.Operator):
    bl_idname = 'gdquest_vse.copy_strips_to_new_scene'
    bl_label = 'Copy strips to new scene'
    bl_description = 'Copy the selected strips to a new scene, \
                      to render a preview or trailer for your video'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({"WARNING"}, "This operator isn't functional yet, operation cancelled")
        return {'CANCELLED'}
        # store cursor position
        # Set cursor to start of selection
        # Copy selection
        # Move cursor back to initial state
        # Create new scene
        # Move cursor to start
        # Paste strips
        # Set preview range
        return {'FINISHED'}