import bpy
from .utils.global_settings import SequenceTypes


class EditCrossfade(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/rCmLhg6.gif)

    Selects the handles of both inputs of a crossfade strip's input and
    calls the grab operator. Allows you to quickly change the location
    of a fade transition between two strips.
    """
    bl_idname = "power_sequencer.edit_crossfade"
    bl_label = "Edit Crossfade"
    bl_description = "Adjust the location of the crossfade between 2 strips"
    bl_options = {'REGISTER', 'UNDO'}

    crossfade_types = ['CROSS', 'GAMMA_CROSS']

    @classmethod
    def poll(cls, context):
        has_active = context.scene.sequence_editor.active_strip
        has_selection = len(context.selected_sequences) > 0
        return has_active or has_selection

    def execute(self, context):
        active = context.scene.sequence_editor.active_strip
        if active.type not in self.crossfade_types:
            effect = self.find_cross_effect(active)
            if not effect:
                return {"CANCELLED"}
            active = context.scene.sequence_editor.active_strip = effect

        bpy.ops.sequencer.select_all(action='DESELECT')
        active.select = True
        active.input_1.select_right_handle = True
        active.input_2.select_left_handle = True
        active.input_1.select = True
        active.input_2.select = True
        bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
        return {'FINISHED'}

    def find_cross_effect(self, sequence):
        """
        Takes a single strip and finds effect strips that use it as input
        Returns the effect strip(s) found as a list, ordered by starting frame
        Returns None if no effect was found
        """
        if sequence.type not in SequenceTypes.VIDEO + SequenceTypes.IMAGE:
            return

        effect_sequences = (s for s in bpy.context.sequences
                            if s.type in SequenceTypes.EFFECT)
        found_effect_strips = []
        for s in effect_sequences:
            if s.input_1.name == sequence.name:
                found_effect_strips.append(s)
            if s.input_count == 2:
                if s.input_2.name == sequence.name:
                    found_effect_strips.append(s)
        for e in found_effect_strips:
            if e.type not in self.crossfade_types:
                continue
            return e
