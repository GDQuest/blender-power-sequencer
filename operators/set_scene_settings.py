import bpy

### set scene settings in one operator
class SetSceneScene(bpy.types.Operator):
    bl_idname = "power_sequencer.set_scene_settings"
    bl_label = "Set Scene Settings"
    bl_description = "Set Settings for Current Scene"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300, height=100)
    
    def check(self, context):
        return True
    
    def draw(self, context):
        rd=bpy.context.scene.render
        layout = self.layout
        
        row = layout.row(align=True)
        row.menu("RENDER_MT_presets", text=bpy.types.RENDER_MT_presets.bl_label)
        row.operator("render.preset_add", text="", icon='ZOOMIN')
        row.operator("render.preset_add", text="", icon='ZOOMOUT').remove_active = True

        col=layout.column(align=True)
        col.label(text="Resolution:")
        col.prop(rd, "resolution_x", text="X")
        col.prop(rd, "resolution_y", text="Y")
        col.prop(rd, "resolution_percentage", text="")
        col.label(text="Aspect Ratio:")
        col.prop(rd, "pixel_aspect_x", text="X")
        col.prop(rd, "pixel_aspect_y", text="Y")
        
        col=layout.column(align=True)
        col.prop(rd, "fps", text="Framerate")
        
    def execute(self, context):
        return {"FINISHED"}
