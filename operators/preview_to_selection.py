import bpy

from .utils.get_frame_range import get_frame_range
from .utils.set_preview_range import set_preview_range
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class PreviewToSelection(bpy.types.Operator):
    """
    *brief* Sets the timeline preview range to that of the selected sequences


    Sets the scene frame start to the earliest frame start of selected sequences and the scene
    frame end to the last frame of selected sequences.
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': 'https://i.imgur.com/EV1sUrn.gif',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'P', 'value': 'PRESS', 'ctrl': True, 'alt': True},
             {},
             'Preview To Selection')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = bpy.context.scene
        selection = bpy.context.selected_sequences
        if not selection:
            return {'CANCELLED'}
        frame_start, frame_end = get_frame_range(
            sequences=bpy.context.selected_sequences, get_from_start=False)

        if scene.frame_start == frame_start and scene.frame_end == frame_end:
            frame_start, frame_end = get_frame_range(get_from_start=True)

        set_preview_range(frame_start, frame_end - 1)
        return {'FINISHED'}

