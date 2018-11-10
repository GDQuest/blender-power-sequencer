import bpy

# select left right
class SelectLeftRight(bpy.types.Operator):
    bl_idname = "power_sequencer.select_left_right"
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

# select left right menu
class SelectLeftRightMenu(bpy.types.Operator):
    bl_idname = "power_sequencer.select_left_right_menu"
    bl_label = "Select Left Right Menu"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    right=bpy.props.BoolProperty(name="Right")

    @classmethod
    def poll(cls, context):
        return bpy.context.area.type=='SEQUENCE_EDITOR' and bpy.context.scene.sequence_editor is not None
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300, height=100)
    
    def check(self, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'right')

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
