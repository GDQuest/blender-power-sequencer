import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class DeselectAllStripsLeftOrRight(bpy.types.Operator):
    """
    Deselects all the strips at the left or right of the time cursor, based on the position
    of the mouse.
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

    side = bpy.props.EnumProperty(
        name="Side",
        description="The side to deselect",
        items=[("mouse", "Mouse position",
                ("Deselect based on the mouse position relative to the"
                 " time cursor")),
               ("left", "Left", "Left of the time cursor"),
               ("right", "Right", "Right of the time cursor")],
        default="mouse")

    @classmethod
    def poll(cls, context):
        return (context.selected_sequences and len(context.selected_sequences) > 0)

    def invoke(self, context, event):
        frame_current = context.scene.frame_current
        frame_mouse = context.region.view2d.region_to_view(
                event.mouse_region_x, 1)[0]

        for s in bpy.context.sequences:
            if frame_mouse < frame_current or self.side == "left":
                if s.frame_final_end < frame_current:
                    self.deselect(s)
            elif frame_mouse >= frame_current or self.side == "right":
                if s.frame_final_start >= frame_current:
                    self.deselect(s)
        return {'FINISHED'}

    def deselect(self, strip):
        strip.select = False
        strip.select_left_handle = False
        strip.select_right_handle = False

