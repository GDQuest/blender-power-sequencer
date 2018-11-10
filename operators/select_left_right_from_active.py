import bpy

# select left right
class SelectLeftRight(bpy.types.Operator):
    bl_idname = "powersequencer.select_left_right"
    bl_label = "Select Left Right"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    right=bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return bpy.context.area.type=='SEQUENCE_EDITOR' and bpy.context.scene.sequence_editor is not None

    def execute(self, context):
        FuncSelectLeftRight(self.right)
        return {"FINISHED"}
    
# select left right function
def FuncSelectLeftRight(right):
    scn=bpy.context.scene
    cf=scn.frame_current
    playing=[]
    channel=[]
    active=0
    for s in scn.sequence_editor.sequences_all:
        s.select=False
        s.select_left_handle=False
        s.select_right_handle=False
        if right==True:
            if s.frame_final_end>cf :
                s.select=True
        else:
            if s.frame_final_start<cf :
                s.select=True
                        
    return {"FINISHED"}
