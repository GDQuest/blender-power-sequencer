import bpy

# toggle audio muted
class ToggleAudioMuted(bpy.types.Operator):
    bl_idname = "power_sequencer.toggle_audio_muted"
    bl_label = "Toggle Audio Playback"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scn=bpy.context.scene
        if scn.use_audio==True:
            scn.use_audio=False
            self.report({'INFO'}, 'Audio UnMuted')
        else:
            scn.use_audio=True
            self.report({'INFO'}, 'Audio Muted')
        return {"FINISHED"}
