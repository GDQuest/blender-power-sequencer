import bpy
from operator import attrgetter
from .utils.global_settings import SequenceTypes


class SnapSelectionToCursor(bpy.types.Operator):
    """Snap selected strips to the cursor, but as a block"""
    bl_idname = "power_sequencer.snap_selection_to_cursor"
    bl_label = "Snap Selection To Cursor"
    bl_description = "Snap selected strips to the cursor as a block"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_sequences) > 0

    def execute(self, context):
        selection = sorted(
            bpy.context.selected_sequences,
            key=attrgetter('frame_final_start'))
        time_move = selection[0].frame_final_start - bpy.context.scene.frame_current
        
        bpy.ops.power_sequencer.select_related_strips()
        bpy.ops.transform.seq_slide(value=(-time_move, 0))
        
        return {'FINISHED'}
