import bpy

from .utils.get_mouse_view_coords import get_mouse_frame_and_channel
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_delete_direct(bpy.types.Operator):
    """
    Delete without confirmation. Replaces default Blender setting
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "",
        "description": doc_description(__doc__),
        "shortcuts": [
            ({"type": "X", "value": "PRESS"}, {}, "Delete Direct"),
            ({"type": "DEL", "value": "PRESS"}, {}, "Delete Direct"),
        ],
        "keymap": "Sequencer",
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc["name"]
    bl_description = doc_brief(doc["description"])
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.sequences and len(context.sequences) > 0

    def invoke(self, context, event):
        frame, channel = get_mouse_frame_and_channel(context, event)
        if not context.selected_sequences:
            bpy.ops.power_sequencer.select_closest_to_mouse(frame=frame, channel=channel)
        return self.execute(context)

    def execute(self, context):
        selection = context.selected_sequences
        if bpy.ops.power_sequencer.crossfade_remove.poll():
            bpy.ops.power_sequencer.crossfade_remove()
        bpy.ops.sequencer.delete()

        report_message = "Deleted " + str(len(selection)) + " sequence"
        report_message += "s" if len(selection) > 1 else ""
        self.report({"INFO"}, report_message)
        return {"FINISHED"}
