import bpy

def find_snap_candidate(frame=0):
    """
    Finds and returns the best frame snap candidate around the frame
    """
    closest_cut_frame = 1000000
    for s in bpy.context.sequences:
        start_to_frame = frame - s.frame_final_start
        end_to_frame = frame - s.frame_final_end
        distance_to_start = abs(start_to_frame)
        distance_to_end = abs(end_to_frame)
        smallest_distance = min(distance_to_start, distance_to_end)

        if smallest_distance == distance_to_start:
            snap_candidate = frame - start_to_frame
        else:
            snap_candidate = frame - end_to_frame

        if abs(frame - snap_candidate) < abs(frame - closest_cut_frame):
            closest_cut_frame = snap_candidate
    return closest_cut_frame
