"""Operators that add animation to the sequences
   These can include fades, transforms, etc."""
import bpy
from bpy.props import BoolProperty, IntProperty, EnumProperty
from .functions.animation import center_img


class FadeStrips(bpy.types.Operator):
    bl_idname = "gdquest_vse.fade_strips"
    bl_label = "Fade strips"
    bl_description = "Fade left, right or both sides of all selected strips \
                      in the VSE"

    bl_options = {'REGISTER', 'UNDO'}

    fade_length = IntProperty(name="Fade length",
                              description="Length of the fade in frames",
                              default=12,
                              min=1)
    fade_type = EnumProperty(
        items=[('both', 'Fade in and out', 'Fade selected strips in and out'),
               ('left', 'Fade in', 'Fade in selected strips'), (
                   'right', 'Fade out', 'Fade out selected strips')],
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
            max_value = s.volume if s.type in SequenceTypes.SOUND \
                        else s.blend_alpha
            fade_create(sequence=s,
                        fade_length=self.fade_length,
                        fade_type=self.fade_type,
                        max_value=max_value)

        self.report({"INFO"}, "Added fade animation to " + str(len(selection))
                    + " sequences.")
        return {"FINISHED"}


class AddTransformEffect(bpy.types.Operator):
    """
    Filters the selection down to image and movie strips.
    Centers images on the screen using the center_img() function.
    Adds a transform effect and sets it to ALPHA_OVER
    for each strip in the selection.
    """
    bl_idname = 'gdquest_vse.add_transform_effect'
    bl_label = 'Add transform effect'
    bl_description = 'Add transform effect to selected image and movie strips. \
                      Auto centers images'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        sequence_editor = bpy.context.scene.sequence_editor
        render = bpy.context.scene.render

        selection = bpy.context.selected_sequences
        selection = [s for s in selection if s.type in ('IMAGE', 'MOVIE')]
        if not selection:
            self.report({"ERROR_INVALID_INPUT"},
                        "No sequences movie or image strips selected")
            return {'CANCELLED'}

        transform_strips = []
        sequencer.select_all(action='DESELECT')
        for s in selection:
            s.mute = True
            if s.type == "IMAGE":
                center_img(s)

            sequence_editor.active_strip = s
            sequencer.effect_strip_add(type='TRANSFORM')

            active = sequence_editor.active_strip
            active.name = "TRANSFORM-%s" % s.name
            active.blend_type = 'ALPHA_OVER'
            transform_strips.append(active)
            active.select = False

        for s in transform_strips:
            s.select = True
        self.report({"INFO"}, "Successfully processed " + str(len(selection)) +
                    " image sequences")
        return {'FINISHED'}


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
