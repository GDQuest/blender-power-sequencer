import bpy
from operator import attrgetter
from .utils.global_settings import SequenceTypes
from .utils.filter_sequences_by_type import filter_sequences_by_type
from .utils.find_next_sequences import find_next_sequences


# TODO: Make it work with 2+ selected strips
# TODO: make it work with pictures and transform strips
# TODO: If source strip has a special blending mode, use that for crossfade?
# TODO: make sure there's no effect on the strip?
# IDEA: If crossfade between effect strips or 2 pictures, set crossfade strip
# ALPHA_OVER
# IDEA: Add custom property to store the name/data_path of the GAMMA_CROSS
# effect added to both strips, so we can detect it later. Why?
class AddCrossfade(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/ZyEd0jD.gif)

    Based on the active strip, finds the closest next sequence
    of a similar type, moves it so it overlaps the active strip,
    and adds a gamma cross effect between them.
    Works with MOVIE, IMAGE and META strips
    """
    bl_idname = "power_sequencer.add_crossfade"
    bl_label = "Add Crossfade"
    bl_description = "Adds cross fade between selected sequence and the closest sequence to it's right"
    bl_options = {"REGISTER", "UNDO"}

    crossfade_duration = bpy.props.FloatProperty(
        name="Crossfade Duration",
        description="The duration of the crossfade",
        default=0.5,
        min=0)
    force_length = bpy.props.BoolProperty(
        name="Force crossfade length",
        description="When true, moves the second strip so the crossfade \
                     is of the length set in 'Crossfade Length'",
        default=True)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        selection = bpy.context.selected_sequences

        scene = context.scene
        fps = scene.render.fps / scene.render.fps_base
        self.crossfade_length = int(self.crossfade_duration * fps)

        if not len(selection) == 1:
            self.report({"ERROR_INVALID_INPUT"}, "Select a single strip to \
            crossfade from")
            return {"CANCELLED"}

        active = bpy.context.scene.sequence_editor.active_strip
        selection = filter_sequences_by_type(selection, SequenceTypes.VIDEO,
                                             SequenceTypes.IMAGE)
        if not selection:
            self.report({"ERROR_INVALID_INPUT"},
                        "Please select a movie, meta or image strip")
            return {"CANCELLED"}
        if selection[0] != active:
            bpy.context.scene.sequence_editor.active_strip = \
                active = selection[0]

        # Find the best strip after active in timeline to crossfade to
        next_sequences = find_next_sequences(selection)
        next_sequences = filter_sequences_by_type(
            next_sequences, SequenceTypes.VIDEO, SequenceTypes.IMAGE)
        if not next_sequences:
            return {"CANCELLED"}
        threshold = active.channel - 1
        higher_sequences = [
            s for s in next_sequences if s.channel >= threshold
        ]
        priority_neighbors = [
            s for s in higher_sequences
            if s.frame_final_start >= active.frame_final_end and
            s.channel - active.channel in (-1, 0, 1)
        ]
        if priority_neighbors:
            neighbor = min(
                priority_neighbors,
                key=attrgetter('frame_final_start', 'channel'))
        elif higher_sequences:
            neighbor = min(
                higher_sequences,
                key=attrgetter('channel', 'frame_final_start'))
        else:
            lower_sequences = [
                s for s in next_sequences if s.channel < threshold
            ]
            neighbor = min(
                lower_sequences,
                key=attrgetter('channel', 'frame_final_start'))

        if self.force_length:
            frame_offset = neighbor.frame_final_start - active.frame_final_end
            neighbor.frame_start -= frame_offset
            neighbor.frame_final_start -= self.crossfade_length
        active.select = True
        neighbor.select = True
        bpy.context.scene.sequence_editor.active_strip = neighbor
        sequencer.effect_strip_add(type='GAMMA_CROSS')
        return {"FINISHED"}
