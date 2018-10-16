import bpy
import operator
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel

class DeleteStripUnderCursor(bpy.types.Operator):
    bl_idname = 'power_sequencer.delete_strip_under_cursor'
    bl_label = 'Delete strip under mouse cursor'
    bl_description = 'If there are not strips selected, the strip that\'s under the mouse cursor will get deleted'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_sequences) == 0
    
    def invoke(self, context, event):
        frame, channel = get_mouse_frame_and_channel(event)

        for s in context.sequences:
            if s.frame_final_start <= frame and s.frame_final_end >= frame and s.channel == channel:
                s.select = True
                bpy.ops.sequencer.delete()
                break

        return {'FINISHED'}

