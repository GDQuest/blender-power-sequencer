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
            s.frame_final_start, channel_offset)

        strip_center_x = (start_x + end_x) / 2
        strip_center_y = (start_y + end_y) / 2
        distance_to_strip = calculate_distance(
            strip_center_x, strip_center_y, mouse_x, mouse_y)
        print("Strip {}, distance: {!s}".format(s.name, distance_to_strip))

        if distance_to_strip < distance_to_closest_strip:
            closest_strip = s
            distance_to_closest_strip = distance_to_strip
    return closest_strip
