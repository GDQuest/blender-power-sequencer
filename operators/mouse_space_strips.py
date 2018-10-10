import bpy
import operator
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel
from .utils.convert_duration_to_frames import convert_duration_to_frames

class MouseSpaceStrips(bpy.types.Operator):
    """
    Offsets all strips to the right of the mouse cursor by a given duration.
    Default shortcut: <kbd>=</kbd>
    """
    bl_idname = 'power_sequencer.mouse_space_strips'
    bl_label = "Space strips after mouse"
    bl_description = "Offsets all strips to the right of the mouse cursor by a given duration"
    bl_options = {'REGISTER', 'UNDO'}

    gap_to_insert = bpy.props.FloatProperty(
        name="Duration",
        description="The time offset to apply to the strips",
        default=1.0)

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0

    def invoke(self, context, event):
        gap_frames = convert_duration_to_frames(self.gap_to_insert)
        strips_to_space = []
        frame, _ = get_mouse_frame_and_channel(event)

        for s in context.sequences:
            if s.frame_final_start >= frame:
                strips_to_space.append(s)

        sorted_strips = sorted(strips_to_space, key=operator.attrgetter('frame_start'), reverse=True)

        for s in sorted_strips:
            s.frame_start += gap_frames
        return {'FINISHED'}
