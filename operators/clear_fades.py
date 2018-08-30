import bpy


class ClearFades(bpy.types.Operator):
    """
    For each selected strip, set opacity to 1.0 and remove any
    opacity-keyframes.
    """
    bl_idname = "power_sequencer.clear_fades"
    bl_label = "Clear Fades"
    bl_description = "Set selected strips' opacity to 1.0 and remove opacity keyframes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if scene.sequence_editor and len(context.selected_sequences) > 0:
            return True
        return False

    def execute(self, context):
        scene = context.scene
        sequence_editor = scene.sequence_editor

        selected = bpy.context.selected_sequences
        fc = bpy.context.scene.animation_data.action.fcurves
        fcurves = scene.animation_data.action.fcurves

        for strip in selected:
            strip.blend_alpha = 1.0
            for curve in fcurves:
                if curve.data_path.endswith("blend_alpha"):
                    if strip == eval(
                            curve.data_path.replace('.blend_alpha', '')):
                        fcurves.remove(curve)
        return {'FINISHED'}
