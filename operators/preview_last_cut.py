import bpy
from .utils.get_frame_range import get_frame_range
from .utils.set_preview_range import set_preview_range


class PreviewLastCut(bpy.types.Operator):
    """
    Finds the closest cut to the time cursor and
    sets the preview to a small range around that frame.
    If the preview matches the range, resets to the full timeline
    """
    bl_idname = 'power_sequencer.preview_last_cut'
    bl_label = 'PS.Preview last cut'
    bl_description = 'Toggle preview around the last cut, based on time cursor'
    bl_options = {'REGISTER', 'UNDO'}

    frame_range = bpy.props.IntProperty(
        name="Preview range",
        description="Total duration of the preview",
        default=24,
        min=1)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = bpy.context.scene
        frame_current = scene.frame_current
        sequences = bpy.context.sequences

        if len(sequences) <= 1:
            return {'CANCELLED'}

        # Find cut closest to time cursor
        last_distance = 100000
        preview_center = 0
        for s in sequences:
            cut = s.frame_final_start
            distance_to_cut = abs(cut - frame_current)
            if distance_to_cut < last_distance:
                last_distance = distance_to_cut
                preview_center = cut

        start = preview_center - self.frame_range / 2
        end = preview_center + self.frame_range / 2
        if preview_center > 1 and start > 1:
            if scene.frame_preview_start == start and scene.frame_preview_end == end:
                start, end = get_frame_range(sequences)
            set_preview_range(start, end)
        return {'FINISHED'}
