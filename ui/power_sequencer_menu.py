import bpy
from ..operators.utils.global_settings import SequenceTypes


class PowerSequencerMenu(bpy.types.Menu):
    bl_label = "Power Sequencer"
    bl_idname = "SEQUENCER_MT_power_sequencer_menu"

    def draw(self, context):
        layout = self.layout

        if not bpy.data.is_saved:
            layout.label('Please save your project')
            layout.operator(
                'wm.save_as_mainfile', icon='SAVE_AS', text='Save as')
            return None

        if not bpy.context.sequences:
            layout.operator(
                'power_sequencer.import_local_footage',
                icon='SEQUENCE',
                text='Import local footage')
            return None

        selection = bpy.context.selected_sequences
        active_strip = bpy.context.scene.sequence_editor.active_strip
        types = set([s.type for s in selection])

        if active_strip.type == 'GAMMA_CROSS':
            layout.operator(
                'power_sequencer.edit_crossfade',
                icon='ACTION_TWEAK',
                text='Edit crossfade')

        for t in types:
            if t in SequenceTypes.VIDEO:
                layout.operator(
                    'power_sequencer.fade_strips',
                    icon='IMAGE_ALPHA',
                    text='Fade strips')
                break

        if len(selection) == 1:
            for s in [active_strip, selection[0]]:
                if s.type in SequenceTypes.VIDEO or s.type in SequenceTypes.IMAGE:
                    layout.separator()
                    layout.operator(
                        'power_sequencer.add_crossfade',
                        icon='IMAGE_ALPHA',
                        text='Auto crossfade')
                    break

        # TODO: Doesn't work from the menu, I guess there's an issue with the invoke method?
        # layout.separator()
        # layout.operator('power_sequencer.grab_closest_handle_or_cut', icon='SNAP_SURFACE', text='Grab cut or handle')

        if len(selection) > 1:
            layout.separator()

            layout.operator(
                'power_sequencer.ripple_delete',
                icon='AUTOMERGE_ON',
                text='Ripple delete')
            layout.operator(
                'power_sequencer.snap_selection_to_cursor',
                icon='SNAP_ON',
                text='Snap selection')

        layout.separator()

        layout.operator(
            'power_sequencer.import_local_footage',
            icon='SEQUENCE',
            text='Import local footage')
        layout.operator(
            'power_sequencer.render_video',
            icon='RENDER_ANIMATION',
            text='Render video for the web')
