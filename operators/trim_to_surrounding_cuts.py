"""
Find the two closest cuts, trims and deletes all strips above in the range but leaves some
margin. Removes the newly formed gap.
"""
import bpy
from math import floor

from .utils.convert_duration_to_frames import convert_duration_to_frames
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_trim_to_surrounding_cuts(bpy.types.Operator):
    """
    Trim to surrounding cuts
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "",
        "description": doc_description(__doc__),
        "shortcuts": [
            (
                {"type": "LEFTMOUSE", "value": "PRESS", "shift": True, "alt": True},
                {},
                "Trim to Surrounding Cuts",
            )
        ],
        "keymap": "Sequencer",
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc["name"]
    bl_description = doc_brief(doc["description"])
    bl_options = {"REGISTER", "UNDO"}

    margin: bpy.props.FloatProperty(
        name="Trim margin",
        description="Margin to leave on either sides of the trim in seconds",
        default=0.2,
        min=0,
    )
    gap_remove: bpy.props.BoolProperty(
        name="Remove gaps",
        description="When trimming the sequences, remove gaps automatically",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return context is not None

    def invoke(self, context, event):
        if not context.sequences:
            return {"CANCELLED"}

        sequencer = bpy.ops.sequencer

        # Convert mouse position to frame, channel
        x = context.region.view2d.region_to_view(x=event.mouse_region_x, y=event.mouse_region_y)[0]
        frame = round(x)

        left_cut_frame, right_cut_frame = self.find_closest_surrounding_cuts(context, frame)
        surrounding_cut_frames_duration = abs(left_cut_frame - right_cut_frame)

        margin_frame = convert_duration_to_frames(context, self.margin)

        if surrounding_cut_frames_duration <= margin_frame * 2:
            self.report(
                {"WARNING"},
                ("The trim margin is larger than the gap\n" "Use snap trim or reduce the margin"),
            )
            return {"CANCELLED"}

        strips_to_delete, strips_to_trim = self.find_strips_in_range(
            context, left_cut_frame, right_cut_frame
        )
        trim_start, trim_end = (left_cut_frame + margin_frame, right_cut_frame - margin_frame)

        # print("start: {!s}, end: {!s}".format(left_cut_frame, right_cut_frame))
        # for s in strips_to_trim:
        #     print(s.name)

        for s in strips_to_trim:
            # If the strip is larger than the range to trim cut it in three
            if s.frame_final_start < trim_start and s.frame_final_end > trim_end:
                sequencer.select_all(action="DESELECT")
                s.select = True
                sequencer.cut(frame=trim_start, type="SOFT", side="RIGHT")
                sequencer.cut(frame=trim_end, type="SOFT", side="LEFT")
                strips_to_delete.append(context.selected_sequences[0])
                continue

            if s.frame_final_start < trim_end and s.frame_final_end > trim_end:
                s.frame_final_start = trim_end
            elif s.frame_final_end > trim_start and s.frame_final_start < trim_start:
                s.frame_final_end = trim_start

        # Delete all sequences that are between the cuts
        sequencer.select_all(action="DESELECT")
        for s in strips_to_delete:
            s.select = True
        sequencer.delete()

        if self.gap_remove:
            frame_to_remove_gap = right_cut_frame - 1 if frame == right_cut_frame else frame
            # bpy.ops.anim.change_frame(frame_to_remove_gap)
            context.scene.frame_current = frame_to_remove_gap
            bpy.ops.power_sequencer.gap_remove()
            context.scene.frame_current = trim_start
        return {"FINISHED"}

    def find_strips_in_range(
        self, context, start_frame, end_frame, sequences=None, find_overlapping=True
    ):
        """
        Returns strips which start and end within a certain frame range, or that overlap a
        certain frame range
        Args:
        - start_frame, the start of the frame range
        - end_frame, the end of the frame range
        - sequences (optional): only work with these sequences.
        If it doesn't receive any, the function works with all the sequences in the current context
        - find_overlapping (optional): find and return a list of strips that overlap the
          frame range

        Returns a tuple of two lists:
        [0], strips entirely in the frame range
        [1], strips that only overlap the frame range
        """
        strips_in_range = []
        strips_overlapping_range = []
        if not sequences:
            sequences = context.sequences
        for s in sequences:
            if start_frame <= s.frame_final_start <= end_frame:
                if start_frame <= s.frame_final_end <= end_frame:
                    strips_in_range.append(s)
                elif find_overlapping:
                    strips_overlapping_range.append(s)
            elif find_overlapping and start_frame <= s.frame_final_end <= end_frame:
                strips_overlapping_range.append(s)
            if s.frame_final_start < start_frame and s.frame_final_end > end_frame:
                strips_overlapping_range.append(s)
        return strips_in_range, strips_overlapping_range

    def find_closest_surrounding_cuts(self, context, frame=0):
        """
        Returns a tuple of (left_cut_frame, right_cut_frame) of the two closest cuts
        surrounding a frame
        Args:
        - frame, find the closest cuts that surround this frame
        """
        start_cut_frame, end_cut_frame = 1000000, 1000000
        for s in context.sequences:
            distance_to_start = abs(frame - s.frame_final_start)
            distance_to_end = abs(frame - s.frame_final_end)

            distance_to_start_cut_frame = abs(start_cut_frame - frame)
            distance_to_end_cut_frame = abs(end_cut_frame - frame)

            if s.frame_final_start < frame and distance_to_start < distance_to_start_cut_frame:
                start_cut_frame = s.frame_final_start
            if s.frame_final_end < frame and distance_to_end < distance_to_start_cut_frame:
                start_cut_frame = s.frame_final_end
            if s.frame_final_end > frame and distance_to_end < distance_to_end_cut_frame:
                end_cut_frame = s.frame_final_end
            if s.frame_final_start > frame and distance_to_start < distance_to_end_cut_frame:
                end_cut_frame = s.frame_final_start
        return start_cut_frame, end_cut_frame
