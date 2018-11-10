import bpy

from .utils.find_strips_mouse import find_strips_mouse
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class SelectClosestToMouse(bpy.types.Operator):
    """
    Select the closest strip under the mouse cursor
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    frame = bpy.props.IntProperty(name="Frame")
    channel = bpy.props.IntProperty(name="Channel")

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        self.frame, self.channel = get_mouse_frame_and_channel(event)
        return self.execute(context)

    def execute(self, context):
        try:
            strip = find_strips_mouse(self.frame, self.channel)[0]
            strip.select = True
        except Exception:
            return {"CANCELLED"}
        return {"FINISHED"}

