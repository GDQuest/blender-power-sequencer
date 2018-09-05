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
        effects = [s for s in context.sequences
                   if s.type in SequenceTypes.EFFECT]
        found_effects = self.find_related_effects(context.selected_sequences, effects)
        effects_to_select = list(found_effects)
        while len(found_effects) > 0:
            found_effects = self.find_related_effects(found_effects, effects)
            effects_to_select.extend(found_effects)

        for e in effects_to_select:
            e.select = True

        # found_inputs = self.find_related_inputs(context.selected_sequences, effects)
        # inputs_to_select = list(found_inputs)
        # while len(found_inputs) > 0:
        #     found_inputs = self.find_related_inputs(found_inputs)
        #     inputs_to_select.extend(found_inputs)

        # for i in inputs_to_select:
        #     i.select = True
        return {'FINISHED'}

    def find_related_effects(self, sequences, effects):
        found = []
        for s in sequences:
            for e in effects:
                try:
                    if e.input_1 == s:
                        found.append(e)
                except Exception:
                    continue
                try:
                    if e.input_2 == s:
                        found.append(e)
                except Exception:
                    continue
        return found

    # Won't work: you need to only select inputs related to the starting selection
    # def find_related_inputs(self, sequences, effects):
    #     found_inputs = []
    #     for e in effects:
    #         try:
    #             found_inputs.append(e.input_1)
    #         except Exception:
    #             pass
    #         try:
    #             found_inputs.append(e.input_2)
    #         except Exception:
    #             pass
    #     return found_inputs
