import bpy
from operator import attrgetter
from .utils.global_settings import SequenceTypes
from .utils.slice_contiguous_sequence_list import slice_selection


class RemoveGaps(bpy.types.Operator):
    bl_idname = 'power_sequencer.remove_gaps'
    bl_label = 'Remove Gaps'
    bl_description = "Remove gaps, starting from the first frame, with the ability to ignore locked strips"

    bl_options = {'REGISTER', 'UNDO'}

    ignore_locked = bpy.props.BoolProperty(
        name="Ignore Locked Strips",
        description="Remove gaps without moving locked strips",
        default=True)
    all = bpy.props.BoolProperty(
        name="Remove All",
        description="Remove all gaps starting from the time cursor",
        default=False)

    frame_start_override = -1

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0

    def execute(self, context):
        frame_start = self.frame_start_override if self.frame_start_override > -1 else context.scene.frame_current

        sequences_to_process = [s for s in context.sequences if not s.lock] if self.ignore_locked else context.sequences
        sequences_to_process = [s for s in sequences_to_process if s.frame_final_start >= frame_start or s.frame_final_end > frame_start]
        if not sequences_to_process:
            return {'CANCELLED'}
        sequence_blocks = slice_selection(sequences_to_process)

        first_gap_frame = self.find_first_gap_frame(sequence_blocks[0], frame_start)
        if first_gap_frame == None:
            return {'FINISHED'}

        first_block_start = min(sequence_blocks[0], key=attrgetter('frame_final_start')).frame_final_start
        blocks_after_gap = sequence_blocks[1:] if first_block_start <= first_gap_frame else sequence_blocks
        self.remove_gaps(blocks_after_gap, first_gap_frame)
        return {'FINISHED'}

    def find_first_gap_frame(self, sorted_sequences, frame_start):
        strips_before_start = [s for s in bpy.context.sequences if s.frame_final_end <= frame_start]

        end_frame_before_gap = 0
        if strips_before_start:
            end_frame_before_gap = max(strips_before_start, key=attrgetter('frame_final_end')).frame_final_end
        strips_start = min(sorted_sequences, key=attrgetter('frame_final_start')).frame_final_start
        strips_end = max(sorted_sequences, key=attrgetter('frame_final_end')).frame_final_end

        if strips_start > frame_start:
            return end_frame_before_gap if end_frame_before_gap < strips_start else frame_start
        else:
            return strips_end

    def remove_gaps(self, sequence_blocks, gap_frame_start):
        for block in sequence_blocks:
            gap_size = block[0].frame_final_start - gap_frame_start
            if gap_size < 1:
                continue
            for s in block:
                try:
                    s.frame_start -= gap_size
                except AttributeError:
                    pass
            self.move_markers(gap_frame_start, gap_size)
            if not self.all:
                break
            gap_frame_start = block[-1].frame_final_end

    def move_markers(self, gap_frame_start, gap_size):
        markers = (m for m in bpy.context.scene.timeline_markers if m.frame > gap_frame_start)
        for m in markers:
            m.frame -= min({gap_size, m.frame - gap_frame_start})
