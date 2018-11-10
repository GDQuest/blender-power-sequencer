import bpy

# toggle audio scrubbing
class ToggleAudioScrubbing(bpy.types.Operator):
    bl_idname = "power_sequencer.toggle_audio_scrubbing"
    bl_label = "Toggle Audio Scrubbing"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scn=bpy.context.scene
        if scn.use_audio_scrub==True:
            scn.use_audio_scrub=False
            self.report({'INFO'}, 'Audio Scrubbing Off')
        else:
            scn.use_audio_scrub=True
            self.report({'INFO'}, 'Audio Scrubbing On')
        return {"FINISHED"}
