import bpy


class PowerSequencerPanel(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_label = "Power Sequencer"
    bl_idname = "SEQUENCER_MT_power_sequencer_panel"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.space_data.view_type == 'SEQUENCER'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator(
            'power_sequencer.ripple_delete',
            icon='AUTOMERGE_ON',
            text='Ripple delete')
