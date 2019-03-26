import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description
from .utils.global_settings import SequenceTypes


class POWER_SEQUENCER_OT_fade_clear(bpy.types.Operator):
    """
    Set strip opacity to 1.0 and remove all opacity-keyframes
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'F', 'value': 'PRESS', 'alt': True, 'ctrl': True}, {}, 'Clear Fades')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.scene.sequence_editor
                and len(context.selected_sequences) > 0)

    def execute(self, context):
        selected = context.selected_sequences
        fcurves = context.scene.animation_data.action.fcurves

        for strip in selected:
            strip.blend_alpha = 1.0
            fade_type = 'volume' if strip.type in SequenceTypes.SOUND else 'blend_alpha'
            for curve in fcurves:
                if not curve.data_path.endswith(fade_type):
                    continue
                # Ensure the fcurve corresponds to the selected strip
                if strip == eval("bpy.context.scene." + curve.data_path.replace('.' + fade_type, '')):
                    fcurves.remove(curve)
        return {'FINISHED'}
