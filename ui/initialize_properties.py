import bpy


class PowerSequencerProperties(bpy.types.PropertyGroup):
    playback_speed: bpy.props.EnumProperty(
        items=[('normal', 'Normal (1x)', ''), ('fast', 'Fast (1.33x)', ''),
               ('faster', 'Faster (1.66x)', ''), ('double', 'Double (2x)', ''),
               ('triple', 'Triple (3x)', '')],
        name='Playback Speed',
        default='normal'
        )

    frame_pre: bpy.props.IntProperty(name='Frame before frame_change', default=0, min=0)

    active_tab: bpy.props.StringProperty(
        name="Active Tab",
        description="The name of the active tab in the UI",
        default="Sequencer"
        )


def initialize_properties():
    bpy.types.Scene.power_sequencer = bpy.props.PointerProperty(
        type=PowerSequencerProperties)
