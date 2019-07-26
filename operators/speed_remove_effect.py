import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_unspeed(bpy.types.Operator):
    """
    *brief* Removes speed from META, un-groups META


    This is the opposite of power_sequencer's "Add Speed" operator.  It seeks out and removes
    the speed modifier inside a meta and ungroups all the remaining strips within.
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "",
        "description": doc_description(__doc__),
        "shortcuts": [],
        "keymap": "Sequencer",
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc["name"]
    bl_description = doc_brief(doc["description"])
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        result = False
        try:
            scene = context.scene
            active_strip = scene.sequence_editor.active_strip
            result = active_strip.select and active_strip.type == "META"
            result = result and [s for s in active_strip.sequences if s.type == "SPEED"]
        except AttributeError:
            pass
        return result

    def execute(self, context):
        active = context.scene.sequence_editor.active_strip
        sub_strips = []
        for s in active.sequences:
            if s.type == "SPEED":
                speed_strip = s
            else:
                sub_strips.append(s)

        bpy.ops.sequencer.meta_separate()
        bpy.ops.sequencer.select_all(action="DESELECT")

        speed_strip.select = True
        bpy.ops.sequencer.delete()

        for s in sub_strips:
            s.select = True
        return {"FINISHED"}
