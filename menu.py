import bpy
from .functions.sequences import SequenceTypes

# TODO: Make the menu contextual, based on the selection size and sequence types
class PowerSequencerMenu(bpy.types.Menu):
    bl_label = "Power Sequencer Menu"
    bl_idname = "SEQUENCER_MT_power_sequencer_menu"

    def draw(self, context):
        layout = self.layout

        selection = bpy.context.selected_sequences
        single_selected = len(selection) == 1

        if len(selection) >= 1:
            first_sequence = selection[0]
            if single_selected and first_sequence.type == 'GAMMA_CROSS':
                layout.operator('power_sequencer.edit_crossfade', icon='ACTION_TWEAK', text='Edit crossfade')
            else:
                layout.operator('power_sequencer.fade_strips', icon='IMAGE_ALPHA', text='Fade strips')

            layout.separator()

            if single_selected and first_sequence.type in SequenceTypes.VIDEO or first_sequence.type in SequenceTypes.IMAGE:
                layout.operator('power_sequencer.add_crossfade', icon='IMAGE_ALPHA', text='Add crossfade')

            layout.separator()

            layout.operator('power_sequencer.ripple_delete', icon='AUTOMERGE_ON', text='Ripple delete')

            layout.separator()

        layout.operator('power_sequencer.import_local_footage', icon='SEQUENCE', text='Import local footage')
        layout.operator('power_sequencer.render_video', icon='RENDER_ANIMATION', text='Render video for the web')
