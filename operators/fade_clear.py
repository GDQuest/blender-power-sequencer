import bpy


class FadeClear(bpy.types.Operator):
    """
    For each selected strip, set opacity to 1.0 and remove any
    opacity-keyframes.
    """
    bl_idname = "power_sequencer.fade_clear"
    bl_label = "Clear Fades"
    bl_description = "Set selected strips' opacity to 1.0 and remove opacity keyframes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.sequence_editor and len(context.selected_sequences) > 0

    def execute(self, context):
        sequence_editor = context.scene.sequence_editor
        selected = context.selected_sequences
        fc = context.scene.animation_data.action.fcurves
        fcurves = context.scene.animation_data.action.fcurves

        for strip in selected:
            strip.blend_alpha = 1.0
            for curve in fcurves:
                if not curve.data_path.endswith("blend_alpha"):
                    continue
                if strip == eval(curve.data_path.replace('.blend_alpha', '')):
                    fcurves.remove(curve)
        return {'FINISHED'}
