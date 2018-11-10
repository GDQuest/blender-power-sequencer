import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class SetTimelineRange(bpy.types.Operator):
    """
    Set the timeline start and end frame using the time cursor
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

    adjust = bpy.props.EnumProperty(
        items=[('start', 'start', 'start'), ('end', 'end', 'end')],
        name='Adjust',
        description='Change the start or the end frame of the timeline',
        default='start')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = bpy.context.scene
        if self.adjust == 'start':
            scene.frame_start = scene.frame_current
        elif self.adjust == 'end':
            scene.frame_end = scene.frame_current - 1
        return {'FINISHED'}

