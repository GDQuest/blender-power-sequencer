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
    remove_all = bpy.props.BoolProperty(
        name="Remove All",
        description="Remove all gaps starting from the time cursor",
        default=False)

    frame_start_override = -1

    @classmethod
    def poll(cls, context):
        return len(context.sequences) > 0

    def execute(self, context):
        frame_start = self.frame_start_override if self.frame_start_override > -1 else context.scene.frame_current

        sequences_to_process = (s for s in context.sequences if s.frame_final_start >= frame_start or s.frame_final_end > frame_start)
        sequence_blocks = slice_selection(sequences_to_process)
        # DEBUG prints
        # print("%s sequence blocks found" % len(sequence_blocks))
        # for block in sequence_blocks:
        #     print("Block start {!s}, end {!s}, len {!s}".format(block[0].frame_final_start, block[-1].frame_final_end, len(block)))

        first_gap_frame = self.find_first_gap_frame(sequence_blocks[0], frame_start)
        if first_gap_frame == None:
            return {'FINISHED'}
        print(first_gap_frame)

        self.remove_gaps(sequence_blocks[1:], first_gap_frame, self.remove_all)
        return {'FINISHED'}

    def find_first_gap_frame(self, sorted_sequences, frame_start):
        sequences_frame_start = min(sorted_sequences, key=attrgetter('frame_final_start')).frame_final_start
        sequences_frame_end = max(sorted_sequences, key=attrgetter('frame_final_end')).frame_final_end
        return frame_start if sequences_frame_start > frame_start else sequences_frame_end

    def remove_gaps(self, sequence_blocks, gap_frame_start, remove_all=False):
        for block in sequence_blocks:
            gap_size = block[0].frame_final_start - gap_frame_start
            # print("Gap size: %s" % gap_size)
            if gap_size < 1:
                continue
            for s in block:
                try:
                    s.frame_start -= gap_size
                except AttributeError:
                    pass
            if not self.remove_all:
                break
            gap_frame_start = block[-1].frame_final_end

    def find_sequences_after_gap(self, sorted_sequences, first_gap_frame):
        after_gap = []
        if self.ignore_locked:
            after_gap = [s for s in sorted_sequences
                            if s.frame_final_start >= first_gap_frame and
                            not s.lock]
        else:
            after_gap = [s for s in sorted_sequences
                            if s.frame_final_start >= first_gap_frame]
        return after_gap
