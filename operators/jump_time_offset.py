import bpy

from .utils.convert_duration_to_frames import convert_duration_to_frames
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class JumpTimeOffset(bpy.types.Operator):
    """
    *brief* Jump forward or backward in time


    Move the time cursor forward or backward, using a duration in seconds.

    The equivalent tool in Blender only works with frames, meaning the jump
    will be different if your project's framerate is different. This tool
    fixes that issue.
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'RIGHT_ARROW', 'value': 'PRESS', 'shift': True},
             {'direction': 'forward'},
             'Jump Forward'),
            ({'type': 'LEFT_ARROW', 'value': 'PRESS', 'shift': True},
             {'direction': 'backward'},
             'Jump Backward')
        ],
        'keymap': 'Frames'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER'}

    duration = bpy.props.FloatProperty(
        name="Duration",
        description="The length of the jump in seconds (default: 1.0)",
        default=1.0,
        min=0)
    direction = bpy.props.EnumProperty(
        name="Direction",
        description="Jump direction, either forward or backward",
        items=[("forward", "Forward", "Jump forward in time"),
               ("backward", "Backward", "Jump backward in time")])

    @classmethod
    def poll(cls, context):
        return context is not None

    def execute(self, context):
        direction = 1 if self.direction == 'forward' else -1
        context.scene.frame_current += (
            convert_duration_to_frames(context, self.duration)
            * direction
        )
        return {'FINISHED'}

