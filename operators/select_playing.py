import bpy

# select playing
class SelectPlaying(bpy.types.Operator):
    bl_idname = "power_sequencer.select_playing"
    bl_label = "Select Playing Clips"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    all=bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return bpy.context.area.type=='SEQUENCE_EDITOR' and bpy.context.scene.sequence_editor is not None

    def execute(self, context):
        FuncSelectPlaying(self.all)
        return {"FINISHED"}
    

# select playing function
def FuncSelectPlaying(all):
    scn=bpy.context.scene
    cf=scn.frame_current
    active=''
    for s in scn.sequence_editor.sequences_all:
        s.select=False
        s.select_left_handle=False
        s.select_right_handle=False
    playing=return_playing_function()
    if len(playing)!=0:
        for s in playing:
            if s.mute==False and active=='':
                active=s
            if all==True:
                s.select=True
            else:
                if active!='':
                    active.select=True
        if active!='':
            scn.sequence_editor.active_strip=active
    return {"FINISHED"}
