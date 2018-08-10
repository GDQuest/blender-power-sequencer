import bpy
import operator

class DeselectSemiTimeline(bpy.types.Operator):
    """
    Deselects all the strips at the left or right of the time cursor, based 
    on the position of the mouse.
    """
    bl_idname = "power_sequencer.deselect_semi_timeline"
    bl_label = "Deselect Semi Timeline"
    bl_description = """Deselects all the strips at the left or right of the 
                        time cursor, based on the position of the mouse."""
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_sequences) > 0

    def invoke(self, context, event):
        time_cursor = context.scene.frame_current
        left_region = self.is_mouse_left(context, event)
        comp = operator.lt if left_region else operator.gt
        for s in context.sequences:
            if comp(self.strip_frame(s, left_region), time_cursor):
                s.select = False

        return {'FINISHED'}
    
    def is_mouse_left(self, context, event):
        """
        Indicates if the mouse in at the left of the time cursor.
        Returns True if the mouse is at the left of the time cursor, otherwise 
        False.
        """
        
        view2d = context.region.view2d
        time_cursor_x = view2d.view_to_region(context.scene.frame_current, 1)[0]
        mouse_x = event.mouse_region_x
        
        return time_cursor_x - mouse_x > 0
    
    def strip_frame(self, strip, at_left, strategy=2):
        """
        Represents a strip by a frame, using various strategies, based on the
        region the strip lies.
        Args:
        - strip: The strip to extract a frame representation of it.
        - at_left: True, to indicate that the mouse lies at the left of the
                   time cursor, or False for right of the time cursor.
        - strategy: The strategy number to be used in the frame representation
                    of the strip. 1 to use the frame_final_end if at_left is 
                    True or to use frame_final_start if at_left is False.
                    Defaults to 2.
        Returns The frame representation of the strip.
        """
    
        if 1 == strategy:
            return strip.frame_final_end if at_left else strip.frame_final_start
        elif 2 == strategy:
            return int((strip.frame_final_start + strip.frame_final_end) / 2)
        else:
            #Default, in case strategy number is not in the list
            return int((strip.frame_final_start + strip.frame_final_end) / 2)
