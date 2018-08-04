import bpy
from .calculate_distance import calculate_distance


def find_closest_strip(sequences, mouse_x, mouse_y):
    view2d = bpy.context.region.view2d

    closest_strip = None
    distance_to_closest_strip = 1000000

    for s in sequences:
        channel_offset = s.channel + 0.5
        start_x, start_y = view2d.view_to_region(
            s.frame_final_start, channel_offset)
        end_x, end_y = view2d.view_to_region(
            s.frame_final_end, channel_offset)

        distance_to_left_handle = calculate_distance(
            start_x, start_y, mouse_x, mouse_y)
        distance_to_right_handle = calculate_distance(
            end_x, end_y, mouse_x, mouse_y)

        distance_smallest = min(distance_to_left_handle, distance_to_right_handle)
        if distance_smallest < distance_to_closest_strip:
            # print("Smallest distance: {}, {!s}".format(s.name, distance_smallest))
            closest_strip = s
            distance_to_closest_strip = distance_smallest
    return closest_strip
