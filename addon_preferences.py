"""
Add-on preferences and interface in the Blender preferences window.
"""
import bpy
from bpy.props import BoolProperty, IntProperty, EnumProperty, StringProperty
from . import addon_updater_ops


class ProxyPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    video_export_path = StringProperty(
        name="Video render folder",
        description="Relative folder to save videos rendered with the add-on",
        default="")

    # addon updater preferences
    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
        )
    updater_intrval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
        )
    updater_intrval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=1,
        min=0,
        max=31
        )
    updater_intrval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
        )
    updater_intrval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
        )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "video_export_path")

        # updater draw function
        addon_updater_ops.update_settings_ui(self, context)
