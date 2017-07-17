"""
Add-on preferences and interface in the Blender preferences window.
"""
import bpy
from bpy.props import BoolProperty, IntProperty, EnumProperty, StringProperty


# TODO: Add button and function to register keymaps
class GeneralProperties(bpy.types.PropertyGroup):
    playback_speed = EnumProperty(items=[
        ('1', 'normal', 'Normal playback speed'),
        ('1.5', 'fast', '1.5 times normal playback speed'),
        ('2', 'very fast', '2 times normal playback speed')],
        name='Playback speed',
        description='',
        default='1')


class ProxyPreferences(bpy.types.AddonPreferences):
    bl_idname = "power_sequencer"

    video_export_path = StringProperty(
        name="Video render folder",
        description="Relative folder to save videos rendered with the add-on",
        default="")
    auto_render_proxies = BoolProperty(
        name="Create proxies automatically",
        description="Automatically build proxies for video sequences on import",
        default=False)
    use_custom_folder = BoolProperty(
        name="Custom proxy folder",
        description="Use a specific folder to store proxies",
        default=False)
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

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "video_export_path")
        layout.prop(self, "auto_render_proxies")
        layout.prop(self, "use_custom_folder")
        layout.prop(self, "custom_folder_path")