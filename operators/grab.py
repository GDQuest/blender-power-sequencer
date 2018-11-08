import bpy

from .utils.get_mouse_view_coords import get_mouse_frame_and_channel
from .utils.global_settings import SequenceTypes
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class Grab(bpy.types.Operator):
    """
    *brief* Grab and move sequences. Extends Blender's built-in grab tool


    Grab and move sequences. If you have no strips selected, it automatically
    finds the strip closest to the mouse and selects it. If you only select
    one or multiple crossfades, selects the handles on either side of the
    crossfades before moving sequences
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': ['G']
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context is not None

    def invoke(self, context, event):
        frame, channel = get_mouse_frame_and_channel(event)
        if not context.selected_sequences:
            bpy.ops.power_sequencer.select_closest_to_mouse(frame=frame,
                                                            channel=channel)
        return self.execute(context)

    def execute(self, context):
        first_sequence = bpy.context.selected_sequences[0]
        if len(bpy.context.selected_sequences) == 1 \
           and first_sequence.type in SequenceTypes.TRANSITION:
            bpy.context.scene.sequence_editor.active_strip = first_sequence
            return bpy.ops.power_sequencer.crossfade_edit()
        return bpy.ops.transform.seq_slide('INVOKE_DEFAULT')

