import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class PlaybackSpeedSet(bpy.types.Operator):
    """
    Change the playback_speed property using an operator property. Used with keymaps
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'ONE', 'value': 'PRESS'}, {'speed': 'normal'}, 'Speed to 1x'),
            ({'type': 'TWO', 'value': 'PRESS'}, {'speed': 'fast'}, 'Speed to 1.33x'),
            ({'type': 'THREE', 'value': 'PRESS'}, {'speed': 'faster'}, 'Speed to 1.66x'),
            ({'type': 'FOUR', 'value': 'PRESS'}, {'speed': 'double'}, 'Speed to 2x'),
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {"REGISTER"}

    speed = bpy.props.EnumProperty(
        items=[('normal', 'Normal (1x)', ''), ('fast', 'Fast (1.33x)', ''),
               ('faster', 'Faster (1.66x)', ''), ('double', 'Double (2x)', ''),
               ('triple', 'Triple (3x)', '')],
        name='Speed',
        description='Change the playback speed',
        default='double')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.scene.power_sequencer.playback_speed = self.speed
        return {"FINISHED"}
