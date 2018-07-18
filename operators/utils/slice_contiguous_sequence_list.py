def slice_selection(sorted_sequences):
    """
    Takes a list of sorted_sequences (by frame_final_start)
    and breaks it down into multiple lists of connected sequences

    Returns a list of lists of sequences,
    each list corresponding to a block of sequences
    that are connected in time.
    """
    # Find when 2 sequences are not connected in time
    break_ids = [0]
    last_sequence = sorted_sequences[0]
    last_biggest_frame_end = last_sequence.frame_final_end
    index = 0
    for s in sorted_sequences:
        if s.frame_final_start > last_biggest_frame_end + 1:
            break_ids.append(index)
        last_biggest_frame_end = max(last_biggest_frame_end, s.frame_final_end)
        last_sequence = s
        index += 1

    # Create lists
    break_ids.append(len(sorted_sequences))
    cuts_count = len(break_ids) - 1
    broken_selection = []
    index = 0
    while index < cuts_count:
        temp_list = []
        index_range = range(break_ids[index], break_ids[index + 1] - 1)
        if len(index_range) == 0:
            temp_list.append(sorted_sequences[break_ids[index]])
        else:
            for counter in range(break_ids[index], break_ids[index + 1]):
                temp_list.append(sorted_sequences[counter])
        if temp_list:
            broken_selection.append(temp_list)
        index += 1
    return broken_selection
