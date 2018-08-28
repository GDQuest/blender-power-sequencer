import bpy
from operator import attrgetter
from .utils.global_settings import SequenceTypes


class CrossfadeRemove(bpy.types.Operator):
    """
    Delete a crossfade strip and moves the handles of the input
    strips to form a cut again
    """
    bl_idname = "power_sequencer.crossfade_remove"
    bl_label = "Remove Crossfade"
    bl_description = "Delete a crossfade strip and moves the handles of the input strips to form a cut again"
    bl_options = {"REGISTER", "UNDO"}

    sequences_override = []

    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_sequences) > 0

    def execute(self, context):
        to_process = self.sequences_override or bpy.context.selected_sequences
        sequences = [s for s in to_process if s.type in SequenceTypes.TRANSITION]
        bpy.ops.sequencer.select_all(action='DESELECT')
        for sequence in sequences:
            effect_middle_frame = round((sequence.frame_final_start + sequence.frame_final_end) / 2)

            inputs = [sequence.input_1, sequence.input_2]
            strip_1 = min(inputs, key=attrgetter('frame_final_end'))
            strip_2 = max(inputs, key=attrgetter('frame_final_end'))

            strip_1.frame_final_end = effect_middle_frame
            strip_2.frame_final_start = effect_middle_frame

            sequence.select = True
            bpy.ops.sequencer.delete()
        return {'FINISHED'}
