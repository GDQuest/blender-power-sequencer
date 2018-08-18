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

    @classmethod
    def poll(cls, context):
        active_strip = bpy.context.scene.sequence_editor.active_strip
        return len(bpy.context.selected_sequences) == 1 \
            and active_strip.type in SequenceTypes.TRANSITION \
            and active_strip.select

    def execute(self, context):
        effect = bpy.context.scene.sequence_editor.active_strip
        effect_middle_frame = round((effect.frame_final_start + effect.frame_final_end) / 2)

        inputs = [effect.input_1, effect.input_2]
        strip_1 = min(inputs, key=attrgetter('frame_final_end'))
        strip_2 = max(inputs, key=attrgetter('frame_final_end'))

        strip_1.frame_final_end = effect_middle_frame
        strip_2.frame_final_start = effect_middle_frame
        bpy.ops.sequencer.delete()
        return {'FINISHED'}
