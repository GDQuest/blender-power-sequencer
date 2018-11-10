import bpy

# go to in out
class GoToInOut(bpy.types.Operator):
    bl_idname = "power_sequencer.go_to_in_out"
    bl_label = "Go to Strip In Out"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    out=bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return bpy.context.area.type=='SEQUENCE_EDITOR' and bpy.context.scene.sequence_editor is not None

    def execute(self, context):
        FuncGoToInOut(self.out)
        return {"FINISHED"}
    
# go to in out function
def FuncGoToInOut(out):
    scn=bpy.context.scene
    cf=scn.frame_current
    selected=[]
    for s in scn.sequence_editor.sequences_all:
        if s.select==True:
            selected.append([s.frame_final_start, s.frame_final_end])
    if len(selected)!=0:
        if out==False:
            scn.frame_current=min(selected,key=itemgetter(0))[0]
        else:
            scn.frame_current=max(selected,key=itemgetter(1))[1]
                                
    return {"FINISHED"}
