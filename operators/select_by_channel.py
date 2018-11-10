import bpy

### Select Operator for shorcut settings
class SelectByChannel(bpy.types.Operator):
    bl_idname = "powersequencer.select_channel"
    bl_label = "Select Channel"
    bl_description = "Select or Deselect entire VSE channel"
    bl_options = {"REGISTER", "UNDO"}
    
    add=bpy.props.BoolProperty(description="Add to current Selection")
    channel=bpy.props.IntProperty(min=1, max=32, description="Channel to Select")

    @classmethod
    def poll(cls, context):
        return bpy.context.area.type=='SEQUENCE_EDITOR' and bpy.context.scene.sequence_editor is not None
    
    def execute(self, context):
        FuncSelectByChannel(self.add, self.channel)
        return {"FINISHED"}
    
### Selection menu
class SelectByChannelMenu(bpy.types.Operator):
    bl_idname = "powersequencer.select_channel_menu"
    bl_label = "Select Channel"
    bl_description = "Select or Deselect entire VSE channel"
    bl_options = {"REGISTER", "UNDO"}
    
    add=bpy.props.BoolProperty()
    channel=bpy.props.IntProperty(min=1, max=32)

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
        layout.prop(self, 'add')
        layout.prop(self, 'channel')

    def execute(self, context):
        FuncSelectByChannel(self.add, self.channel)
        return {"FINISHED"}
    
# select by channel function
def FuncSelectByChannel(add, channel):
    scn=bpy.context.scene
    channelstrip=[]
    chk=0
    for s in scn.sequence_editor.sequences_all:
        if add==False:
            s.select=False
            s.select_left_handle=False
            s.select_right_handle=False
        if s.channel==channel:
            if add==False:
                s.select=True
            else:
                channelstrip.append(s)
                if s.select==True:
                    chk=1
    if add==True:
        if chk==0:
            for s in channelstrip:
                s.select=True
        else:
            for s in channelstrip:
                s.select=False
                s.select_left_handle=False
                s.select_right_handle=False
    return {"FINISHED"}
