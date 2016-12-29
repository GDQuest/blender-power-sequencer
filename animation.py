"""Operators that add animation to the sequences
   These can include fades, transforms, etc."""
import bpy
from bpy.props import BoolProperty, IntProperty, EnumProperty


# TODO: Smart filtering of the selection: apply fades to parent effects?
class FadeStrips(bpy.types.Operator):
    bl_idname = "gdquest_vse.fade_strips"
    bl_label = "Fade strips"
    bl_description = "Fade left, right or both sides of all selected strips in the VSE"
    bl_options = {'REGISTER', 'UNDO'}

    fade_length = IntProperty(
        name="Fade length",
        description="Length of the fade in frames",
        default=12,
        min=1)
    fade_type = EnumProperty(
        items=[('both', 'Fade in and out', 'Fade selected strips in and out'),
               ('left', 'Fade in', 'Fade in selected strips'),
               ('right', 'Fade out', 'Fade out selected strips')],
        name="Fade type",
        description="Fade in, out, or both in and out. Default is both.",
        default='both')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        from .functions.animation import fade_create

        selected_sequences = bpy.context.selected_sequences
        selection = selected_sequences if len(selected_sequences) > 0 \
            else bpy.context.scene.sequence_editor.active_strip
        sequence_count = fade_create(selection, self.fade_length, self.fade_type)
        
        if sequence_count:
            self.report({"INFO"}, "Added fade animation to " + str(sequence_count) + " sequences.")
        return {"FINISHED"}


# TODO: Find which animation data to store and how to store it
class AddAnimationFromLibrary(bpy.types.Operator):
    bl_idname = "gdquest_vse.animation_library"
    bl_label = "Animation library"
    bl_description = "Adds animation to selected strips."
    bl_options = {"REGISTER", "UNDO"}

    both_sides = BoolProperty(
        name="Both sides",
        description="Animate both the start and the end of the strip",
        default=True)
    # TODO: Get the presets from a subfolder/file
    presets = None

    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        return {"FINISHED"}
