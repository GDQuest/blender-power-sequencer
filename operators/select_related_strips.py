import bpy
from .utils.global_settings import SequenceTypes

class SelectRelatedStrips(bpy.types.Operator):
    """
    Find and select effects related to the selection,
    but also inputs of selected effects. This helps to then copy
    or duplicate strips with all attached effects.
    """
    bl_idname = 'power_sequencer.select_related_strips'
    bl_label = 'Select Related Strips'
    bl_description = "Find and select effect strips applied to selected strips"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_sequences) > 0

    def execute(self, context):
        effects = [s for s in bpy.context.sequences
                   if s.type in SequenceTypes.EFFECT]

        selected_effects = [s for s in bpy.context.selected_sequences
                            if s.type in SequenceTypes.EFFECT]
        for e in selected_effects:
            e.input_1.select = True
            try:
                e.input_2.select = True
            except Exception:
                pass

        for s in bpy.context.selected_sequences:
            for e in effects:
                if e.input_1 == s:
                    e.select = True
                    continue
                try:
                    if e.input_2 == s:
                        e.select = True
                except Exception:
                    continue
        return {'FINISHED'}
