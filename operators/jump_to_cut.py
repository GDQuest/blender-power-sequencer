import bpy
from operator import attrgetter

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class JumpToCut(bpy.types.Operator):
    """
    *brief* Jump to next/previous cut


    Jump to the next or the previous cut in the edit.  Unlike Blender's default tool, also
    works during playback.
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [],
        'keymap': 'Frames'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    direction = bpy.props.EnumProperty(
        name="Direction",
        description="Jump direction, either forward or backward",
        items=[("forward", "Forward", "Jump forward in time"),
               ("backward", "Backward", "Jump backward in time")])

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0

    def execute(self, context):
        jump_to_frame = None
        frame_current = context.scene.frame_current
        sorted_sequences = sorted(context.sequences,
                                  key=attrgetter('frame_final_start'))
        if self.direction == 'forward':
            for s in sorted_sequences:
                if s.frame_final_end <= frame_current:
                    continue
                jump_to_frame = (s.frame_final_end
                                 if s.frame_final_start <= frame_current else
                                 s.frame_final_start)
                break
        if self.direction == 'backward':
            for s in reversed(sorted_sequences):
                if s.frame_final_start >= frame_current:
                    continue
                jump_to_frame = (s.frame_final_start
                                 if s.frame_final_end >= frame_current else
                                 s.frame_final_end)
                break

        if jump_to_frame:
            context.scene.frame_current = max(1, jump_to_frame)
        return {'FINISHED'}

