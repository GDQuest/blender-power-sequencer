import bpy


class SelectStripsUnderCursor(bpy.types.Operator):
    bl_idname = 'power_sequencer.select_strips_under_cursor'
    bl_label = 'Select strips under cursor'
    bl_description = "Selects the strips that are currently under the time cursor"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0
    
    def execute(self, context):
        current_frame = context.scene.frame_current
        sequences_to_select = []
        for s in context.sequences:
            if s.frame_final_start <= current_frame and s.frame_final_end >= current_frame:
                sequences_to_select.append(s)
        if not sequences_to_select:
            return {'CANCELLED'}
        for s in sequences_to_select:
            s.select = True
        return {'FINISHED'}
        
