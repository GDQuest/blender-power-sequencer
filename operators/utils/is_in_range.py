def is_in_range(sequence, start, end):
    """
    Checks if a single sequence's start or end is in the range

    Args:
    - sequence: the sequence to check for
    - start, end: the start and end frames
    Returns True if the sequence is within the range, False otherwise
    """
    s_start = sequence.frame_final_start
    s_end = sequence.frame_final_end
    return start <= s_start <= end or start <= s_end <= end