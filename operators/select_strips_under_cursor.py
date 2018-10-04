import bpy


class SelectStripsUnderCursor(bpy.types.Operator):
    bl_idname = 'power_sequencer.select_strips_under_cursor'
    bl_label = 'Select strips under cursor'
    bl_description = "Selects the strips that are currently under the time cursor"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        if len(context.sequences) == 0:
            self.report({'INFO'}, "No sequences found")
            return {'CANCELLED'}

        current_frame = context.scene.frame_current
        selected_sequences = 0
        for s in context.sequences:
            final = s.frame_start + s.frame_duration
            if s.frame_start <= current_frame and final >= current_frame:
                s.select = True
                selected_sequences += 1
        if selected_sequences == 0:
            self.report({'INFO'}, "No sequences under the cursor - none selected")
            return {'CANCELLED'}

        return {'FINISHED'}
        
