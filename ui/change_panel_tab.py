import bpy


class ChangePanelTab(bpy.types.Operator):
    """
    Change which Tab is active and which set of addon buttons are
    currently visible
    """
    bl_idname = "power_sequencer.change_panel_tab"
    bl_label = "Change Panel Tab"
    bl_description = "Change visibility of Power Sequencer operations"

    active_tab = bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene
        scene.power_sequencer.active_tab = self.active_tab

        return {"FINISHED"}
