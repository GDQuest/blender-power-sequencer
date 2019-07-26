import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description
from .utils.global_settings import SequenceTypes


class POWER_SEQUENCER_OT_fade_clear(bpy.types.Operator):
    """
    *brief* Removes fade animation from selected sequences.

    Removes opacity or volume animation on selected sequences and resets the
    property to a value of 1.0. Works on all types of sequences.
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "",
        "description": doc_description(__doc__),
        "shortcuts": [
            ({"type": "F", "value": "PRESS", "alt": True, "ctrl": True}, {}, "Clear Fades")
        ],
        "keymap": "Sequencer",
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc["name"]
    bl_description = doc_brief(doc["description"])
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len(context.selected_sequences) > 0

    def execute(self, context):
        fcurves = context.scene.animation_data.action.fcurves

        for sequence in context.selected_sequences:
            animated_property = "volume" if hasattr(sequence, "volume") else "blend_alpha"
            for curve in fcurves:
                if not curve.data_path.endswith(animated_property):
                    continue
                # Ensure the fcurve corresponds to the selected sequence
                if sequence == eval(
                    "bpy.context.scene." + curve.data_path.replace("." + animated_property, "")
                ):
                    fcurves.remove(curve)
            setattr(sequence, animated_property, 1.0)

        return {"FINISHED"}
