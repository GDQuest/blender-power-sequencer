def find_sequences_after(context, sequence):
    """
    Finds the strips following the sequences passed to the function
    Args:
    - Sequences, the sequences to check
    Returns all the strips after the sequence in the current context
    """
    sequence_start = sequence.frame_final_start
    return [s for s in context.sequences if s.frame_final_start > sequence_start]
