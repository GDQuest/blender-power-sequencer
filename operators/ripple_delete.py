import bpy
from operator import attrgetter
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel
from .utils.slice_contiguous_sequence_list import slice_selection
from .utils.get_frame_range import get_frame_range


class RippleDelete(bpy.types.Operator):
    bl_idname = 'power_sequencer.ripple_delete'
    bl_label = 'Ripple Delete'
    bl_description = 'Delete the selected sequences and remove gaps'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.sequences

    def invoke(self, context, event):
        frame, channel = get_mouse_frame_and_channel(event)
        if not context.selected_sequences:
            bpy.ops.power_sequencer.select_closest_to_mouse(frame=frame, channel=channel)
        return self.execute(context)

    def execute(self, context):
        scene = bpy.context.scene
        sequencer = bpy.ops.sequencer
        selection = bpy.context.selected_sequences

        if not selection:
            return {'CANCELLED'}

        selection_length = len(selection)
        cursor_start = scene.frame_current
        cursor_offset = 0

        channels = set((s.channel for s in selection))

        audio_scrub = bpy.context.scene.use_audio_scrub
        if audio_scrub:
            bpy.context.scene.use_audio_scrub = False

        # If only 1 block of strips, we store linked strips
        selection_blocks = slice_selection(selection)

        surrounding_strips = []
        is_single_channel = len(selection_blocks) == 1 and len(channels) == 1
        if is_single_channel:
            bpy.ops.sequencer.select_linked()
            for s in bpy.context.selected_sequences:
                if s not in selection:
                    surrounding_strips.append(s)
            sequencer.select_all(action='DESELECT')
            for s in selection_blocks[0]:
                s.select = True
            sequencer.delete()
        else:
            for block in selection_blocks:
                sequencer.select_all(action='DESELECT')
                for s in block:
                    s.select = True
                selection_start, _ = get_frame_range(block)
                sequencer.delete()

                scene.frame_current = selection_start
                bpy.ops.power_sequencer.remove_gaps()
            # auto move cursor back
            if bpy.context.screen.is_animation_playing and len(
                    selection_blocks) == 1:
                sequences = selection_blocks[0]
                start_frame = min(
                    sequences,
                    key=attrgetter('frame_final_start')).frame_final_start
                end_frame = max(
                    sequences,
                    key=attrgetter('frame_final_end')).frame_final_end
                delete_duration = end_frame - start_frame
                if scene.frame_current > start_frame:
                    cursor_offset = delete_duration

        # Concatenate
        if is_single_channel:
            for s in surrounding_strips:
                s.select = True
            bpy.ops.power_sequencer.concatenate_strips()

        scene.frame_current = cursor_start - cursor_offset
        report_message = 'Deleted ' + str(selection_length) + ' sequence'
        report_message += 's' if selection_length > 1 else ''
        self.report({'INFO'}, report_message)
        if audio_scrub:
            bpy.context.scene.use_audio_scrub = audio_scrub

        return {'FINISHED'}
