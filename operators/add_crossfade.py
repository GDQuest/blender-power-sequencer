import bpy
from operator import attrgetter
from .utils.find_next_sequences import find_next_sequences
from .utils.convert_duration_to_frames import convert_duration_to_frames


# TODO: make it work with pictures and transform strips
# TODO: If source strip has a special blending mode, use that for crossfade?
# TODO: make sure there's no effect on the strip?
class AddCrossfade(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/ZyEd0jD.gif)

    Finds the closest sequence after the active strip,
    of a similar type, moves it next to the selected strip (optional)
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
    auto_move_strip = bpy.props.BoolProperty(
        name="Auto Move Strip",
        description="When true, moves the second strip so the crossfade \
                     is of the length set in 'Crossfade Length'",
        default=True)

    @classmethod
    def poll(cls, context):
        return bpy.context.scene.sequence_editor.active_strip

    def execute(self, context):
        active = bpy.context.scene.sequence_editor.active_strip
        crossfade_length = convert_duration_to_frames(self.crossfade_duration)
        print(len(bpy.context.sequences))
        print(len(bpy.context.scene.sequence_editor.sequences))
        next_in_channel = [
            s for s in find_next_sequences(active)
            if s.channel == active.channel
        ]
        if not next_in_channel:
            return {'CANCELLED'}
        next_sequence = min(next_in_channel, key=attrgetter('frame_final_start'))
        if not next_sequence:
            return {'CANCELLED'}

        if self.auto_move_strip:
            frame_offset = next_sequence.frame_final_start - active.frame_final_end
            next_sequence.frame_start -= frame_offset

        if next_sequence.frame_final_start == active.frame_final_end:
            next_sequence.frame_final_start += crossfade_length / 2
            active.frame_final_end -= crossfade_length / 2
        active.select = True
        next_sequence.select = True
        bpy.context.scene.sequence_editor.active_strip = next_sequence
        bpy.ops.sequencer.effect_strip_add(type='GAMMA_CROSS')
        return {"FINISHED"}
