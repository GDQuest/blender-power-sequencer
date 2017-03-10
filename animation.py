"""Operators that add animation to the sequences
   These can include fades, transforms, etc."""
import bpy
from bpy.props import BoolProperty, IntProperty, EnumProperty


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
        selection = bpy.context.selected_sequences
        if not selection:
            return {"CANCELLED"}

        from .functions.animation import fade_create
        from .functions.sequences import SequenceTypes
        for s in selection:
            max_value = s.volume if s.type in SequenceTypes.SOUND else s.blend_alpha 
            fade_create(sequence=s, fade_length=self.fade_length, fade_type=self.fade_type, max_value=max_value)

        self.report({"INFO"}, "Added fade animation to " + str(len(selection)) + " sequences.")
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
