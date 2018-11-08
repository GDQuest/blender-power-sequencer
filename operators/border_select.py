import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class BorderSelect(bpy.types.Operator):
    """
    *brief* Wrapper around Blender's border select, deselects handles


    Deselects the strips' handles before applying border select, so you don't
    have to deselect manually first.
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': ['Shift B; Border Select']
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    extend = bpy.props.BoolProperty(
        name="Extend the selection",
        description=("Extend the current selection if checked,"
                     " otherwise clear it"),
        default=False)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for s in bpy.context.selected_sequences:
            s.select_right_handle = False
            s.select_left_handle = False
        bpy.ops.sequencer.select_border('INVOKE_DEFAULT', extend=self.extend)
        return {'FINISHED'}

