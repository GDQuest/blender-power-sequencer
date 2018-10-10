import bpy
import operator
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel
from .utils.convert_duration_to_frames import convert_duration_to_frames

class MouseSpaceStrips(bpy.types.Operator):
    bl_idname = 'power_sequencer.mouse_space_strips'
    bl_label = 'Space strips after mouse'
    bl_description = 'Pushes everything after the mouse position reliably - even during playback'
    bl_options = {'REGISTER', 'UNDO'}

    gap_to_insert = bpy.props.FloatProperty(
        name="Gap to add",
        description="The amount of seconds to add to the strips",
        default=2)

    @classmethod
    def poll(cls, context):
        return True
    
    def invoke(self, context, event):
        gap_frames = convert_duration_to_frames(self.gap_to_insert)
        strips_to_space = []
        frame, channel = get_mouse_frame_and_channel(event)
        
        for s in context.sequences:
            if s.frame_final_start >= frame:
                strips_to_space.append(s)
        
        sorted_strips = sorted(strips_to_space, key=operator.attrgetter('frame_start'), reverse = True)
        
        for s in sorted_strips:
            s.frame_start += gap_frames

        return {'FINISHED'}

