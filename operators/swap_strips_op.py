import bpy
from .utils.swap_strips import swap_strips

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

    def poll(cls, context):
        return len(bpy.context.selected_sequences) == 2

    def execute(self, context):
        selected_strips = bpy.context.selected_sequences
        if swap_strips(selected_strips[0], selected_strips[1]):
            return {'FINISHED'}
        else:
            return {"CANCELLED"}
