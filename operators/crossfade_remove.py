import bpy
from operator import attrgetter

from .utils.global_settings import SequenceTypes
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_crossfade_remove(bpy.types.Operator):
    """
    Delete a crossfade strip and moves the handles of the input strips to form a cut again
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {"REGISTER", "UNDO"}

    sequences_override = []

    @classmethod
    def poll(cls, context):
        return (context.selected_sequences
                and len([s for s in context.selected_sequences
                         if s.type in SequenceTypes.TRANSITION]) > 0)

    def execute(self, context):
        to_process = (self.sequences_override
                      if self.sequences_override else
                      context.selected_sequences)
        sequences = [s for s in to_process
                     if s.type in SequenceTypes.TRANSITION]
        if not sequences:
            return {'FINISHED'}
        bpy.ops.sequencer.select_all(action='DESELECT')
        for sequence in sequences:
            effect_middle_frame = round((sequence.frame_final_start
                                         + sequence.frame_final_end) / 2)

            inputs = [sequence.input_1, sequence.input_2]
            strip_1 = min(inputs, key=attrgetter('frame_final_end'))
            strip_2 = max(inputs, key=attrgetter('frame_final_end'))

            strip_1.frame_final_end = effect_middle_frame
            strip_2.frame_final_start = effect_middle_frame

            sequence.select = True
            bpy.ops.sequencer.delete()
        return {'FINISHED'}

