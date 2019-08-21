import bpy
from math import ceil

from .utils.global_settings import SequenceTypes
from .utils.functions import slice_selection
from .utils.functions import find_linked
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_speed_up_movie_strip(bpy.types.Operator):
    """
    *brief* Adds a speed effect to the  2x speed, set frame end, wrap both into META

    Add 2x speed to strip and set its frame end accordingly. Wraps both the strip and the speed
    modifier into a META strip.
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "https://i.imgur.com/ZyEd0jD.gif",
        "description": doc_description(__doc__),
        "shortcuts": [({"type": "PLUS", "value": "PRESS", "shift": True}, {}, "Add Speed")],
        "keymap": "Sequencer",
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc["name"]
    bl_description = doc_brief(doc["description"])
    bl_options = {"REGISTER", "UNDO"}

    speed_factor: bpy.props.IntProperty(
        name="Speed factor", description="How many times the footage gets sped up", default=2, min=0
    )
    individual_sequences: bpy.props.BoolProperty(
        name="Affect individual strips",
        description="Speed up every VIDEO strip individually",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def execute(self, context):
        sequences = [s for s in context.selected_sequences if s.type in SequenceTypes.VIDEO]

        if not sequences:
            self.report(
                {"ERROR_INVALID_INPUT"},
                "No Movie sequence or Metastrips selected. Operation cancelled",
            )
            return {"FINISHED"}

        selection_blocks = []
        if self.individual_sequences:
            selection_blocks = [[s] for s in sequences]
        else:
            selection_blocks = slice_selection(context, sequences)

        for sequences in selection_blocks:
            bpy.ops.sequencer.select_all(action="DESELECT")
            self.speed_effect_add(context, sequences)

        self.report(
            {"INFO"}, "Successfully processed " + str(len(selection_blocks)) + " selection blocks"
        )
        return {"FINISHED"}

    def speed_effect_add(self, context, sequences=[]):
        if not sequences:
            return

        sequence_editor = context.scene.sequence_editor
        sequence = None
        if len(sequences) == 1:
            sequence = sequence_editor.active_strip = sequences[0]
        else:
            for s in sequences:
                s.select = True
            bpy.ops.sequencer.meta_make()
            sequence = sequence_editor.active_strip

        bpy.ops.sequencer.effect_strip_add(type="SPEED")
        speed_effect = sequence_editor.active_strip
        speed_effect.use_default_fade = False
        speed_effect.speed_factor = self.speed_factor

        duration = ceil(sequence.frame_final_duration / speed_effect.speed_factor)
        sequence.frame_final_end = sequence.frame_final_start + duration

        sequence_editor.active_strip = sequence
        bpy.ops.sequencer.select_all(action="DESELECT")
        sequence.select = True
        speed_effect.select = True
        bpy.ops.sequencer.meta_make()

        sequence_editor.active_strip.name = sequence.name + " " + str(self.speed_factor) + "x"
