import bpy

# TODO: Make the menu contextual, based on the selection size and sequence types
class PowerSequencerMenu(bpy.types.Menu):
    bl_label = "Power Sequencer Menu"
    bl_idname = "SEQUENCER_MT_power_sequencer_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator('power_sequencer.fade_strips', icon='IMAGE_ALPHA', text='Fade strips')
        layout.operator('power_sequencer.add_crossfade', icon='IMAGE_ALPHA', text='Add crossfade')
        layout.operator('power_sequencer.edit_crossfade', icon='ACTION_TWEAK', text='Edit crossfade')
        layout.operator('power_sequencer.ripple_delete', icon='AUTOMERGE_ON', text='Ripple delete')
        layout.operator('power_sequencer.import_local_footage', icon='SEQUENCE', text='Import local footage')
        layout.operator('power_sequencer.render_video', icon='RENDER_ANIMATION', text='Render video for the web')
