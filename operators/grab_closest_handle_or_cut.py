"""
Selects and grabs the strip handle or cut closest to the mouse cursor.
Hover near a cut and use this operator to slide it.
"""
import bpy

from math import floor
from operator import attrgetter

from .utils.calculate_distance import calculate_distance


class GrabClosestCut(bpy.types.Operator):
    bl_idname = "power_sequencer.grab_closest_cut"
    bl_label = "Grab Closest Cut"
    bl_description = "Grab the handles that form the closest cut"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context is not None

    def invoke(self, context, event):
        if not bpy.context.sequences:
            return {'CANCELLED'}

        sequencer = bpy.ops.sequencer

        mouse_x, mouse_y = event.mouse_region_x, event.mouse_region_y
        frame, channel = self.find_cut_closest_to_mouse(mouse_x, mouse_y)

        matching_sequences = []
        for s in bpy.context.sequences:
            if not s.channel == channel:
                continue
            if abs(s.frame_final_start - frame) <= 1 or abs(
                    s.frame_final_end - frame) <= 1:
                matching_sequences.append(s)
        matching_count = len(matching_sequences)

        sequencer.select_all(action='DESELECT')
        if matching_count != 2:
            return bpy.ops.power_sequencer.grab_sequence_handle()
            # sequence = matching_sequences[0]
            # sequence.select = True
            # if abs(sequence.frame_final_start - frame) <= 1:
            #     sequence.select_left_handle = True
            # elif abs(sequence.frame_final_end - frame) <= 1:
            #     sequence.select_right_handle = True

        sorted_sequences = sorted(matching_sequences,
                                  key=attrgetter('frame_final_start'))
        for s in matching_sequences:
            s.select = True
        sorted_sequences[0].select_right_handle = True
        sorted_sequences[1].select_left_handle = True
        return bpy.ops.transform.seq_slide('INVOKE_DEFAULT')

    def find_cut_closest_to_mouse(self, mouse_x, mouse_y):
        """
        takes the mouse's coordinates in the sequencer area and returns the two strips
        who share the cut closest to the mouse
        Use it to find the handle(s) to select with the grab on the fly operator
        """
        view2d = bpy.context.region.view2d

        closest_cut = (None, None)
        distance_to_closest_cut = 1000000.0

        for s in bpy.context.sequences:
            channel_offset = s.channel + 0.5
            start_x, start_y = view2d.view_to_region(
                s.frame_final_start, channel_offset)
            end_x, end_y = view2d.view_to_region(
                s.frame_final_start, channel_offset)

            distance_to_start = calculate_distance(
                start_x, start_y, mouse_x, mouse_y)
            distance_to_end = calculate_distance(
                end_x, end_y, mouse_x, mouse_y)

            if distance_to_start < distance_to_closest_cut:
                closest_cut = (start_x, start_y)
                distance_to_closest_cut = distance_to_start
            if distance_to_end < distance_to_closest_cut:
                closest_cut = (end_x, end_y)
                distance_to_closest_cut = distance_to_end

        closest_cut_local_coords = view2d.region_to_view(
            closest_cut[0], closest_cut[1])
        frame, channel = round(closest_cut_local_coords[0]), floor(
            closest_cut_local_coords[1])
        return frame, channel
