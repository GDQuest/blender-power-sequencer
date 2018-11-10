import bpy

# move selected strip for key binding
class MoveSelectedClips(bpy.types.Operator):
    bl_idname = "powersequencer.move_clips"
    bl_label = "Move selected Clips"
    bl_description = "Move selected clips"
    bl_options = {"REGISTER", "UNDO"}
    
    forward=bpy.props.BoolProperty()
    ten_frames=bpy.props.BoolProperty()
    vertical=bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        return bpy.context.area.type=='SEQUENCE_EDITOR' and bpy.context.scene.sequence_editor is not None

    def execute(self, context):
        if self.vertical==True:
            if self.forward==True:
                bpy.ops.transform.seq_slide(value=(0, 1)) 
            else:
                bpy.ops.transform.seq_slide(value=(0, -1)) 
        else:
            if self.forward==True and self.ten_frames==False:
                bpy.ops.transform.seq_slide(value=(1, 0))    
            elif self.forward==True and self.ten_frames==True:
                bpy.ops.transform.seq_slide(value=(10, 0))
            elif self.forward==False and self.ten_frames==False:
                bpy.ops.transform.seq_slide(value=(-1, 0))
            elif self.forward==False and self.ten_frames==True:
                bpy.ops.transform.seq_slide(value=(-10, 0))

        return {"FINISHED"}
