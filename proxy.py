"""Proxy-related operators
   The add-on produces proxy video files using ffmpeg,
   and offers more flexibility than the built-in proxies
   for simple video projects (online videos, tutorials, vlogs...)."""
import os
import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty

# TODO: store and update proxies function (store/update paths to proxy folders and files)
# TODO: clear proxies (delete all proxy files)
# Prompt for confirmation


# Sets video strips as proxies
# TODO: Add settings in addon prefs
# TODO: Make use of SettingsProxies PropertyGroup
# TODO: If custom dir, store proxies in a subfolder
class SetVideosProxies(bpy.types.Operator):
    bl_idname = "power_sequencer.set_video_proxies"
    bl_label = "PS - Set selected strips as Proxies"
    bl_description = "Set all video strips in the current scene as proxies and rebuild"
    bl_options = {"REGISTER"}

    use_custom_folder = BoolProperty(
        name="Custom proxy folder",
        description="Use a custom folder to store proxies",
        default=True)
    custom_folder_path = StringProperty(
        name="Custom proxy folder path",
        description="Store the generated proxies in a specific folder on your hard drive (absolute path)",
        default=r"D:\Program Files\Blender proxies")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sequencer = bpy.ops.sequencer

        selection = bpy.context.selected_sequences
        if not bpy.context.selected_sequences:
            self.report({"ERROR_INVALID_INPUT"}, "No movie sequences found")
            return {'CANCELLED'}

        prefs = context.user_preferences.addons["power_sequencer"].preferences

        for s in selection:
            if s.type not in ('MOVIE', 'IMAGE'):
                s.select = False

        sequencer.enable_proxies(proxy_25=prefs.proxy_25,
                                 proxy_50=prefs.proxy_50,
                                 proxy_75=prefs.proxy_75,
                                 proxy_100=prefs.proxy_100,
                                 override=False)
        if prefs.use_custom_folder and prefs.custom_folder_path:
            for s in bpy.context.selected_sequences:
                s.proxy.use_proxy_custom_directory = True
                blend_filename = bpy.path.basename(bpy.data.filepath)
                blend_filename = os.path.splitext(blend_filename)[0]
                s.proxy.directory = os.path.join(prefs.custom_folder_path, blend_filename)

        sequencer.rebuild_proxy({'dict': "override"}, 'INVOKE_DEFAULT')
        return {"FINISHED"}


# TODO: Add way to change us
class SettingsProxies(bpy.types.PropertyGroup):
    proxy_on_import = BoolProperty(
        name="Auto create proxy",
        description="Set and build videos strips as proxies on import for all strips",
        default=True)
    use_custom_folder = BoolProperty(
        name="Custom proxy folder",
        description="Use a custom folder to store proxies",
        default=True)
    custom_folder_path = StringProperty(
        name="Custom proxy folder path",
        description="Store the generated proxies in a specific folder on your hard drive (absolute path)",
        default=r"D:\Program Files\Blender proxies")
    proxy_25 = BoolProperty(name="Proxy at 25%", default=True)
    proxy_50 = BoolProperty(name="Proxy at 50%", default=False)
    proxy_75 = BoolProperty(name="Proxy at 75%", default=False)
    proxy_100 = BoolProperty(name="Proxy at 100%", default=False)
    proxy_quality = IntProperty(
        name="Proxy JPG quality",
        default=90, min=1, max=100)


# Panel for proxy options management
def proxy_menu(self, context):
    # prefs = context.user_preferences.addons['power_sequencer'].preferences
    power_sequencer_proxy = context.scene.power_sequencer_proxy

    layout = self.layout

    row = layout.row()
    row.separator()
    row = layout.row()
    row.prop(power_sequencer_proxy, 'proxy_on_import')

    # if prefs.proxy_on_import:
    row = layout.row(align=True)
    row.prop(power_sequencer_proxy, "proxy_25", toggle=True)
    row.prop(power_sequencer_proxy, "proxy_50", toggle=True)
    row.prop(power_sequencer_proxy, "proxy_75", toggle=True)
    row.prop(power_sequencer_proxy, "proxy_100", toggle=True)

    row = layout.row()
    row.prop(power_sequencer_proxy, "proxy_quality")
