import bpy
from bpy.props import FloatProperty, EnumProperty

from .functions.global_settings import SequenceTypes


class SoundToggleWaveform(bpy.types.Operator):
    bl_idname = 'gdquest_vse.sound_toggle_waveform'
    bl_label = 'Sound toggle waveform'
    bl_description = 'Toggle drawing of the waveform for selected strips \
                      or for all strips if no selection is active'
    bl_options = {'REGISTER', 'UNDO'}

    mode = EnumProperty(
        items=[('auto', 'Auto', 'Automatically toggle the waveform'),
               ('on', 'On', 'Make the waveforms visible'),
               ('off', 'Off', 'Make the waveforms invisible')],
        name="Waveform visibility",
        description="Force the waveforms' visibility with On or Off, \
            or let Blender choose automatically",
        default='auto')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = bpy.context.selected_sequences
        if not selection:
            selection = bpy.context.sequences

        sequences = [s for s in selection if s.type in SequenceTypes.SOUND]

        if not sequences:
            self.report({"ERROR_INVALID_INPUT"}, "Select at least one sound strip")
            return {'CANCELLED'}

        show_waveform = None
        if self.mode == 'auto':
            from operator import attrgetter
            from .functions.global_settings import SequenceParams
            show_waveform = not sorted(sequences, key=attrgetter(SequenceParams.FRAME_START))[0].show_waveform
        else:
            show_waveform = True if self.mode == 'on' else False

        for s in sequences:
            s.show_waveform = show_waveform
        return {'FINISHED'}


class SoundSetVolume(bpy.types.Operator):
    bl_idname = 'gdquest_vse.sound_set_volume'
    bl_label = 'Change Sound strips volume'
    bl_description = 'Change the volume of all selected Sound strips (use F6)'
    bl_options = {'REGISTER', 'UNDO'}

    volume = FloatProperty(
        name="Volume",
        description="The volume to use",
        default=1.0,
        min=0.0, max=4.0,
        soft_min=0.0, soft_max=4.0,
        step=5,
        precision=2
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sequences = [s for s in bpy.context.selected_sequences if s.type in SequenceTypes.SOUND]

        for s in sequences:
            s.volume = self.volume
        return {'FINISHED'}