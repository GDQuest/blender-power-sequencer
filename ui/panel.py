import bpy
from bpy.props import StringProperty, EnumProperty, BoolProperty


bpy.types.Scene.video_directory = StringProperty(
        name = "Video Path",
        subtype="DIR_PATH"
)
bpy.types.Scene.proxy_25 = BoolProperty(
    name = "25%",
    description = "Build 25% proxy",
)
bpy.types.Scene.proxy_50 = BoolProperty(
    name="50%",
    description="Build 50% proxy",
)
bpy.types.Scene.proxy_100 = BoolProperty(
    name="100%",
    description="Build 100% proxy",
)
bpy.types.Scene.proxy_preset = EnumProperty(
        name = "Preset",
        description = "Select the preset that you want to use",
        items = [
            ("webm", "webm", "YouTube preset"),
            ("mp4", "mp4", "mp4 preset"),
            ("nvenc", "nvenc", "nvenc preset"),
        ]
)


class Panel(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_label = "Power Sequencer"
    bl_idname = "power_sequencer.panel"
    # bl_options = {"DEFAULT_CLOSED"}

    def __init__(self, *args, **kwargs):
        #initSceneProperties(bpy.context.scene)
        for a in args:
            print(a)

    @classmethod
    def poll(cls, context):
        return context.space_data.view_type == 'SEQUENCER'

    def draw(self, context):
        scene = context.scene
        active_tab = scene.power_sequencer.active_tab
        categories = {
            "Sequencer": "SEQ_SEQUENCER",
            "Render": "RENDER_ANIMATION",
            "Modifier": "MODIFIER",
            "Sound": "SOUND",
        }
        remaining_space = 1.0
        space_per_button = 1.0 / len(categories.keys())

        layout = self.layout
        box = layout.box()
        split = box.row()

        split = split.split(0.0, align=True)
        for i in range(len(categories.keys())):
            category = list(categories.keys())[i]
            icon = categories[category]

            used_space = space_per_button * (i + 1)
            percent = space_per_button / remaining_space

            split = split.split(percentage=percent, align=True)
            remaining_space = 1.0 - used_space

            split.operator(
                "power_sequencer.change_panel_tab",
                text="",
                icon=icon,
                emboss=active_tab != category).active_tab = category

        if scene.power_sequencer.active_tab == "Sequencer":
            row = box.row()
            row.operator('power_sequencer.ripple_delete', icon='AUTOMERGE_ON')

        elif scene.power_sequencer.active_tab == "Render":
            row = box.row()
            row.operator('power_sequencer.generate_proxies')
            row2 = box.row()
            row2.prop(scene, 'proxy_25')
            row2.prop(scene, 'proxy_50')
            row2.prop(scene, 'proxy_100')
            row3 = box.row()
            row3.prop(scene, 'video_directory')
            row4 = box.row()
            row4.prop(scene, 'proxy_preset')

        elif scene.power_sequencer.active_tab == "Modifier":
            row = box.row()
            row.operator('power_sequencer.crossfade_add', icon="IMAGE_ALPHA")

        elif scene.power_sequencer.active_tab == "Sound":
            row = box.row()
            row.label("Sound Functions Here")
