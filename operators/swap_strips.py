import bpy
from operator import attrgetter

class SwapStrips(bpy.types.Operator):
    """
    Swaps the 2 selected strips between them. More specific, places the first
    strip in the channel and starting frame (frame_final_start) of the second
    strip, and places the second strip in the channel and starting frame
    (frame_final_end) of the first strip. If the biggest in duration strip
    doesn't fit in the space of the smallest strip, it does nothing.
    """
    bl_idname = "power_sequencer.swap_strips"
    bl_label = "Swap Strips"
    bl_description = "Swaps the 2 selected strips between them"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_sequences) == 2

    def execute(self, context):
        sorted_strips = sorted(bpy.context.selected_sequences, key=attrgetter('frame_final_duration'))
        small_strip, big_strip = sorted_strips[0], sorted_strips[1]

        if small_strip.frame_final_start < big_strip.frame_final_start and \
           small_strip.channel == big_strip.channel:
            if big_strip.frame_final_start < \
               small_strip.frame_final_start + big_strip.frame_final_duration:
                return {'CANCELLED'}


        # Cancel if there's no space to swap the stips
        if small_strip.frame_final_duration != big_strip.frame_final_duration:
            other_sequences = (s for s in bpy.context.sequences if s not in sorted_strips)
            for s in other_sequences:
                if s.channel != small_strip.channel:
                    continue
                if s.frame_final_end < small_strip.frame_final_start:
                    continue

                if s.frame_final_start < small_strip.frame_final_start + \
                   big_strip.frame_final_duration:
                    return {'CANCELLED'}

        # Swapping the strips
        end_frame = max(bpy.context.sequences, key=attrgetter('frame_final_end')).frame_final_end
        small_strip_start, big_strip_start  = small_strip.frame_final_start, big_strip.frame_final_start

        end_frame += big_strip.frame_final_duration - \
                small_strip.frame_final_duration
        
        # Move both strips to an empty location, otherwise they'll collide upon moving
        self.move_to_frame(small_strip, end_frame)
        self.move_to_frame(big_strip, end_frame + small_strip.frame_final_duration + 1)

        big_strip.channel, small_strip.channel = small_strip.channel, big_strip.channel

        self.move_to_frame(big_strip, small_strip_start)
        self.move_to_frame(small_strip, big_strip_start)
        return {'FINISHED'}

    def move_to_frame(self, strip, frame):
        """
        Moves a strip based on its frame_final_start without changing its
        duration.
        Args:
        - strip: The strip to be moved.
        - frame: The frame, the frame_final_start of the strip will be placed at.
        """
        strip.frame_start = frame + strip.frame_start - strip.frame_final_start
