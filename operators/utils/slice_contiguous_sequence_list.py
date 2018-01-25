from operator import attrgetter


def slice_selection(sequences):
    """
    Takes a list of sequences and breaks it down
    into multiple lists of connected sequences.

    Returns a list of lists of sequences,
    each list corresponding to a block of sequences
    that are connected in time.
    """
    if not sequences:
        raise AttributeError('No sequences passed to the function')

    # Find when 2 sequences are not connected in time
    sequences = sorted(sequences, key=attrgetter('frame_final_start'))

    last_sequence = sequences[0]
    break_ids = [0]
    index = 0
    for s in sequences:
        if s.frame_final_start > last_sequence.frame_final_end + 1:
            break_ids.append(index)
        last_sequence = s
        index += 1

    # Create lists
    break_ids.append(len(sequences))
    cuts_count = len(break_ids) - 1
    broken_selection = []
    index = 0
    while index < cuts_count:
        temp_list = []
        index_range = range(break_ids[index], break_ids[index + 1] - 1)
        if len(index_range) == 0:
            temp_list.append(sequences[break_ids[index]])
        else:
            for counter in range(break_ids[index], break_ids[index + 1]):
                temp_list.append(sequences[counter])
        # print("SPLIT LIST: ")
        # print(str(temp_list))
        # print("\n")
        if temp_list:
            broken_selection.append(temp_list)
        index += 1
    return broken_selection