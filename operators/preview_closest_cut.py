import bpy
from .utils.get_frame_range import get_frame_range
from .utils.set_preview_range import set_preview_range
from .utils.convert_duration_to_frames import convert_duration_to_frames


class PreviewClosestCut(bpy.types.Operator):
    """
    Finds the closest cut to the time cursor and
    sets the preview to a small range around that frame.
    If the preview matches the range, resets to the full timeline
    """
    bl_idname = 'power_sequencer.preview_closest_cut'
    bl_label = "Preview Closest Cut"
    bl_description = "Toggle preview around the closest cut, based on time cursor"
    bl_options = {'REGISTER', 'UNDO'}

    duration = bpy.props.FloatProperty(
        name="Preview duration",
        description="Total duration of the preview, in seconds",
        default=1.0,
        min=0.1)
    cut_frame_override = bpy.props.IntProperty(
        name="Cut Frame Override",
        description="Force to preview around this frame",
        default=0,
        min=0,
        options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return len(bpy.context.sequences) > 0

    def execute(self, context):
        scene = bpy.context.scene

        preview_center = self.find_closest_cut_frame(context) \
                        if not self.cut_frame_override \
                        else self.cut_frame_override

        duration_frame = convert_duration_to_frames(self.duration)
        start = preview_center - duration_frame / 2
        end = preview_center + duration_frame / 2
        if not (preview_center > 1 and start > 1):
            return {'CANCELLED'}

        if scene.frame_preview_start == start and scene.frame_preview_end == end:
            start, end = get_frame_range(context.sequences)
        set_preview_range(start, end)
        return {'FINISHED'}

    def find_closest_cut_frame(self, context):
        last_distance = 100000
        closest_cut_frame = 0
        for s in context.sequences:
            cuts = [s.frame_final_start, s.frame_final_end]
            for cut_frame in cuts:
                distance_to_cut = abs(cut_frame - context.scene.frame_current)
                if distance_to_cut < last_distance:
                    last_distance = distance_to_cut
                    closest_cut_frame = cut_frame
        return closest_cut_frame
