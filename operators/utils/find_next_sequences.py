import bpy
from operator import attrgetter


def find_next_sequences(sequences):
    """
    Finds the strips following the sequences passed to the function
    Args:
    - Sequences, the sequences to check
    Returns all the strips after the sequence in the current context
    """
    if not sequences:
        raise AttributeError('Missing sequences parameter')

    last_seq_start = max(sequences, key=attrgetter('frame_final_start')).frame_final_start

    next_sequences = []
    for s in bpy.context.sequences:
        if s.frame_final_start > last_seq_start:
            next_sequences.append(s)
    return next_sequences