import bpy
from operator import attrgetter


class JumpToCut(bpy.types.Operator):
    """
    Jump to the next or the previous cut in the edit.
    Unlike Blender's default tool, also works during playback.
    """
    bl_idname = 'power_sequencer.jump_to_cut'
    bl_label = 'Jump to Cut'
    bl_description = "Jump to the next or to the previous cut"
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
        frame_current = bpy.context.scene.frame_current
        sorted_sequences = sorted(context.sequences, key=attrgetter('frame_final_start'))
        if self.direction == 'forward':
            for s in sorted_sequences:
                if s.frame_final_end <= frame_current:
                    continue
                jump_to_frame = s.frame_final_end if s.frame_final_start <= frame_current else s.frame_final_start
                break
        if self.direction == 'backward':
            for s in reversed(sorted_sequences):
                if s.frame_final_start >= frame_current:
                    continue
                jump_to_frame = s.frame_final_start if s.frame_final_end >= frame_current else s.frame_final_end
                break

        if jump_to_frame:
            bpy.context.scene.frame_current = max(1, jump_to_frame)
        return {'FINISHED'}
