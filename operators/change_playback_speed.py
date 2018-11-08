import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class ChangePlaybackSpeed(bpy.types.Operator):
    """
    Change the playback_speed property using an operator property. Used with keymaps
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': ['ONE; Speed to 1x',
                      'TWO; Speed to 1.33x',
                      'THREE; Speed to 1.66x',
                      'FOUR; Speed to 2x']
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
        bpy.context.scene.power_sequencer.playback_speed = self.speed
        return {"FINISHED"}

