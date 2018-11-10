import bpy

# select handles
class SelectHandles(bpy.types.Operator):
    bl_idname = "powersequencer.select_handles"
    bl_label = "Select Handles"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    right=bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return bpy.context.area.type=='SEQUENCE_EDITOR' and bpy.context.scene.sequence_editor is not None

    def execute(self, context):
        if self.right==True:
            bpy.ops.sequencer.strip_jump(next=True, center=False)
        else:
            bpy.ops.sequencer.strip_jump(next=False, center=False)
        FuncSelectHandles(self.right)
        return {"FINISHED"}
    
# select handles function
def FuncSelectHandles(right):
    scn=bpy.context.scene
    cf=scn.frame_current
    r_select=[]
    l_select=[]
    channel=[]
    trimlist=[]
    active=0
    for s in scn.sequence_editor.sequences_all:
        s.select=False
        s.select_left_handle=False
        s.select_right_handle=False
        if s.frame_final_start==cf:
            l_select.append(s)
        if s.frame_final_end==cf:
            r_select.append(s)
    for s in r_select:
        s.select=s.select_right_handle=True
    for s in l_select:
        s.select=s.select_left_handle=True
    
    return {"FINISHED"}
