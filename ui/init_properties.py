import bpy


def init_properties():
    """
    Initialize addon properties
    """
    
    
    bpy.types.Scene.power_sequencer_active_tab = bpy.props.StringProperty(
        name="Active Tab",
        description="The name of the active tab in the UI",
        default="Sequencer"
        )
