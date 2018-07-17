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
        return len(context.scene.sequence_editor.sequences) > 0

    def execute(self, context):
        if self.frame_start_override > -1:
            frame_start = self.frame_start_override
        else:
            frame_start = context.scene.frame_current

        sorted_sequences = sorted(context.scene.sequence_editor.sequences, key=attrgetter('frame_final_start'))
        first_sequence_start = sorted_sequences[0].frame_final_start
        if first_sequence_start > frame_start:
            first_gap_frame = frame_start
        else:
            first_gap_frame = -1
            last_sequence = sorted_sequences[0]
            last_biggest_frame_end = last_sequence.frame_final_end
            for s in sorted_sequences:
                if last_biggest_frame_end >= s.frame_final_start:
                    last_sequence = s
                    continue
                elif last_sequence.frame_final_end < s.frame_final_start:
                    first_gap_frame = last_sequence.frame_final_end
                    break
                last_biggest_frame_end = max(last_biggest_frame_end, s.frame_final_end)
                last_sequence = s

        if first_gap_frame == -1:
            return {'FINISHED'}

        sequences_after_gap = []
        if self.ignore_locked:
            sequences_after_gap = [s for s in sorted_sequences
                                   if s.frame_final_start >= first_gap_frame and
                                   not s.lock]
        else:
            sequences_after_gap = [s for s in sorted_sequences
                                   if s.frame_final_start >= first_gap_frame]

        sequence_blocks = slice_selection(sequences_after_gap)
        print("Gap frame: %s" % first_gap_frame)
        print("%s sequence blocks found" % len(sequence_blocks))
        for block in sequence_blocks:
            print("Block start {!s}, end {!s}, len {!s}".format(block[0].frame_final_start, block[-1].frame_final_end, len(block)))


        # FIXME: can't read strips with inputs
        # Apply the same time offset to each sequence_block
        current_gap_start_frame = first_gap_frame
        for sequence_block in sequence_blocks:
            sorted_block = sorted(sequence_block, key=attrgetter('frame_final_start', 'frame_final_end'))
            gap_size = sorted_block[0].frame_final_start - current_gap_start_frame
            # print("Gap size: %s" % gap_size)
            if gap_size < 1:
                continue

            for s in sorted_block:
                try:
                    s.frame_start -= gap_size
                except AttributeError:
                    pass
            if not self.all:
                break
            current_gap_start_frame = sorted_block[-1].frame_final_end
        return {'FINISHED'}
