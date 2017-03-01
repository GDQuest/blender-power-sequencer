"""
Add-on preferences and interface in the Blender preferences window.
"""
import bpy
from bpy.props import EnumProperty, StringProperty


# TODO: Add button and function to register keymaps
class GDquestVSESetting(bpy.types.PropertyGroup):
    playback_speed = EnumProperty(items=[
        ('1', 'normal', 'Normal playback speed'),
        ('1.5', 'fast', '1.5 times normal playback speed'),
        ('2', 'very fast', '2 times normal playback speed')],
        name='Playback speed',
        description='',
        default='1')


class GDquestVSEPreferences(bpy.types.AddonPreferences):
    bl_idname = "gdquest_vse"
    video_export_path = StringProperty(
        name="Video render folder",
        description="Relative folder to save videos rendered with the add-on",
        default="")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "video_export_path")