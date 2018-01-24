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

        row = layout.row()
        row.operator("power_sequencer.import_keymap",
                     icon="LIBRARY_DATA_DIRECT")
        row.operator("power_sequencer.export_keymap",
                     icon="NEW")
        row.operator("power_sequencer.set_default_keymap",
                     icon="RECOVER_LAST")

        layout.prop(self, "video_export_path")
        layout.prop(self, "auto_render_proxies")
        layout.prop(self, "use_custom_folder")
        layout.prop(self, "custom_folder_path")

        # updater draw function
        addon_updater_ops.update_settings_ui(self, context)
