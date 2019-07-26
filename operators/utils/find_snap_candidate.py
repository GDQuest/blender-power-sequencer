def find_snap_candidate(context, frame=0):
    """
    Returns the cut frame closest to the `frame` argument
    """
    snap_candidate = 1000000

    for s in context.sequences:
        start_to_frame = frame - s.frame_final_start
        end_to_frame = frame - s.frame_final_end

        distance_to_start = abs(start_to_frame)
        distance_to_end = abs(end_to_frame)

        candidate = (
            frame - start_to_frame
            if min(distance_to_start, distance_to_end) == distance_to_start
            else frame - end_to_frame
        )

        if abs(frame - candidate) < abs(frame - snap_candidate):
            snap_candidate = candidate

    return snap_candidate
