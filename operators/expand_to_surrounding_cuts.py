import bpy
from math import floor

from .utils.functions import convert_duration_to_frames
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description
from .utils.functions import slice_selection


class POWER_SEQUENCER_OT_expand_to_surrounding_cuts(bpy.types.Operator):
    """
    *Brief* Expand selected strips to surrounding cuts

    Finds potential gaps surrounding each block of selected sequences and extends the corresponding
    sequence handle to it.
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "",
        "description": doc_description(__doc__),
        "shortcuts": [
            ({"type": "E", "value": "PRESS", "ctrl": True}, {}, "Expand to Surrounding Cuts")
        ],
        "keymap": "Sequencer",
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc["name"]
    bl_description = doc_brief(doc["description"])
    bl_options = {"REGISTER", "UNDO"}

    margin: bpy.props.FloatProperty(
        name="Trim margin",
        description="Margin to leave on either sides of the trim in seconds",
        default=0.2,
        min=0,
    )
    gap_remove: bpy.props.BoolProperty(
        name="Remove gaps",
        description="When trimming the sequences, remove gaps automatically",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def invoke(self, context, event):
        sequence_blocks = slice_selection(context, context.selected_sequences)
        for sequences in sequence_blocks:
            seq_first = min(sequences, key=lambda s: s.frame_final_start)
            seq_last = max(sequences, key=lambda s: s.frame_final_end)
            frame_left, frame_right = find_closest_cuts(
                context, sequences, seq_first.frame_final_start, seq_last.frame_final_end
            )

            if (
                seq_first.frame_final_start == frame_left
                and seq_last.frame_final_end == frame_right
            ):
                continue

            seq_first.frame_final_start = (
                frame_left
                if frame_left < seq_first.frame_final_start
                else seq_first.frame_final_start
            )
            seq_last.frame_final_end = (
                frame_right
                if frame_right > seq_first.frame_final_end
                else seq_first.frame_final_end
            )

        return {"FINISHED"}


def find_closest_cuts(context, sequences, frame_min, frame_max):
    frame_left = max(
        context.sequences, key=lambda s: s.frame_final_end if s.frame_final_end <= frame_min else -1
    ).frame_final_end
    frame_right = min(
        context.sequences,
        key=lambda s: s.frame_final_start if s.frame_final_start >= frame_max else 1000000,
    ).frame_final_start
    return frame_left, frame_right
