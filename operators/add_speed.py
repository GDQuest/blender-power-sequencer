import bpy
from .utils.global_settings import SequenceTypes
from .utils.slice_contiguous_sequence_list import slice_selection
from .utils.find_linked_sequences import find_linked


class AddSpeed(bpy.types.Operator):
    bl_idname = "power_sequencer.add_speed"
    bl_label = "Add Speed"
    bl_description = "Adds a speed effect to your clip, sets its speed and \
        size, wraps it into a meta strip set to over drop for easier editing"

    bl_options = {"REGISTER", "UNDO"}

    speed_factor = bpy.props.IntProperty(
        name="Speed factor",
        description="How many times the footage gets sped up",
        default=2,
        min=0)
    individual_sequences = bpy.props.BoolProperty(
        name="Affect individual strips",
        description="Speed up every VIDEO strip individually",
        default=False)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        scene = bpy.context.scene
        active = scene.sequence_editor.active_strip

        # Select linked sequences
        for s in find_linked(bpy.context.selected_sequences):
            s.select = True
        selection = bpy.context.selected_sequences

        video_sequences = [
            s for s in selection if s.type in SequenceTypes.VIDEO
        ]

        if not video_sequences:
            self.report({
                "ERROR_INVALID_INPUT"
            }, "No Movie sequence or Metastrips selected. Operation cancelled")
            return {"CANCELLED"}

        # Slice the selection
        selection_blocks = []
        if self.individual_sequences:
            for s in selection:
                if s.type in SequenceTypes.EFFECT:
                    self.report(
                        {"ERROR_INVALID_INPUT"},
                        "Can't speed up individual sequences if effect strips \
                    are selected. Please only select VIDEO or META strips. \
                    Operation cancelled")
                    return {'CANCELLED'}
            selection_blocks = [[s] for s in video_sequences]
        else:
            selection_blocks = slice_selection(selection)

        for block in selection_blocks:
            # start, end = 0, 0
            sequencer.select_all(action='DESELECT')
            if len(block) == 1:
                active = scene.sequence_editor.active_strip = block[0]
                # TODO: Use the full source clip
                # start = active.frame_final_start / self.speed_factor
                # end = start + active.frame_final_duration / self.speed_factor
                # active.frame_offset_start, active.frame_offset_end = 0, 0
            else:
                for s in block:
                    s.select = True
                # SELECT GROUPED ONLY AFFECTS ACTIVE STRIP
                # bpy.ops.sequencer.select_grouped(type='EFFECT_LINK')
                sequencer.meta_make()
                active = scene.sequence_editor.active_strip
            # Add speed effect
            sequencer.effect_strip_add(type='SPEED')
            effect_strip = bpy.context.scene.sequence_editor.active_strip
            effect_strip.use_default_fade = False
            effect_strip.speed_factor = self.speed_factor

            sequencer.select_all(action='DESELECT')
            active.select_right_handle = True
            active.select = True
            scene.sequence_editor.active_strip = active
            source_name = active.name

            from math import ceil
            size = ceil(
                active.frame_final_duration / effect_strip.speed_factor)
            endFrame = active.frame_final_start + size
            sequencer.snap(frame=endFrame)

            effect_strip.select = True
            sequencer.meta_make()
            bpy.context.selected_sequences[
                0].name = source_name + " " + str(self.speed_factor) + 'x'
        self.report({"INFO"}, "Successfully processed " +
                    str(len(selection_blocks)) + " selection blocks")
        return {"FINISHED"}
