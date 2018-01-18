import bpy
from .utils.global_settings import SequenceTypes


class MakeStillImage(bpy.types.Operator):
    """Converts image under the cursor to a still image, to create
    a pause effect in the video, using the active sequence"""
    bl_idname = "power_sequencer.grab_still_image"
    bl_label = "PS.Grab still image from active strip"
    bl_options = {'REGISTER', 'UNDO'}

    strip_duration = bpy.props.IntProperty(
        name="Strip length",
        description="Length of the new strip in frames",
        default=106)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = bpy.context.scene
        active = scene.sequence_editor.active_strip
        sequencer = bpy.ops.sequencer
        transform = bpy.ops.transform

        start_frame = scene.frame_current
        offset = self.strip_duration

        if active.type not in SequenceTypes.VIDEO:
            self.report({"ERROR_INVALID_INPUT"},
                        "You must select a video or meta strip. \
                You selected a strip of type" + str(active.type) + " instead.")
            return {"CANCELLED"}

        if not active.frame_final_start <= start_frame < \
           active.frame_final_end:
            self.report({"ERROR_INVALID_INPUT"},
                        "Your time cursor must be on the frame you want \
                        to convert to a still image.")
            return {"CANCELLED"}

        if start_frame == active.frame_final_start:
            scene.frame_current = start_frame + 1

        active.select = True
        source_blend_type = active.blend_type
        sequencer.cut(frame=scene.frame_current, type='SOFT', side='RIGHT')
        transform.seq_slide(value=(offset, 0))
        sequencer.cut(
            frame=scene.frame_current + offset + 1, type='SOFT', side='LEFT')
        transform.seq_slide(value=(-offset, 0))

        sequencer.meta_make()
        active = scene.sequence_editor.active_strip
        active.name = 'Still image'
        active.blend_type = source_blend_type
        active.select_right_handle = True
        transform.seq_slide(value=(offset, 0))

        scene.frame_current = start_frame

        active.select = True
        active.select_right_handle = False
        active.select_left_handle = False
        return {"FINISHED"}
