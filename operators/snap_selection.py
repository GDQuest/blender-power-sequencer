import bpy
from .utils.functions import get_sequences_under_cursor
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_snap_selection(bpy.types.Operator):
    """
    *Brief* Snap the entire selection to the time cursor.

    Automatically selects sequences if there is no active selection.
    To snap each strip individually, see Snap.
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "",
        "description": doc_description(__doc__),
        "shortcuts": [
            ({"type": "S", "value": "PRESS", "alt": True}, {}, "Snap selection to cursor")
        ],
        "keymap": "Sequencer",
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc["name"]
    bl_description = doc_brief(doc["description"])
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.sequences

    def execute(self, context):
        sequences = (
            context.selected_sequences
            if len(context.selected_sequences) > 0
            else get_sequences_under_cursor(context)
        )
        time_move = context.scene.frame_current - sequences[0].frame_final_start
        # bpy.ops.power_sequencer.select_related_strips()
        for s in sequences:
            s.frame_start += time_move
        return {"FINISHED"}
