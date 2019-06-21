from .get_frame_range import get_frame_range
from .global_settings import SequenceTypes
from .is_in_range import is_in_range


def find_linked(context, sequences, selected_sequences):
    """
    Takes a list of sequences and returns a list of all the sequences
    and effects that are linked in time

    Args:
    - sequences: a list of sequences

    Returns a list of all the linked sequences, but not the sequences passed to the function
    """
    start, end = get_frame_range(context, sequences, selected_sequences)
    sequences_in_range = [s for s in sequences if is_in_range(context, s, start, end)]
    effects = (s for s in sequences_in_range if s.type in SequenceTypes.EFFECT)
    selected_effects = (s for s in sequences if s.type in SequenceTypes.EFFECT)

    linked_sequences = []

    # Filter down to effects that have at least one of seq as input and
    # Append input sequences that aren't in the source list to linked_sequences
    for e in effects:
        if not hasattr(e, 'input_2'):
            continue
        for s in sequences:
            if e.input_2 == s:
                linked_sequences.append(e)
                if e.input_1 not in sequences:
                    linked_sequences.append(e.input_1)
            elif e.input_1 == s:
                linked_sequences.append(e)
                if e.input_2 not in sequences:
                    linked_sequences.append(e.input_2)

    # Find inputs of selected effects that are not selected
    for e in selected_effects:
        try:
            if e.input_1 not in sequences:
                linked_sequences.append(e.input_1)
            if e.input_count == 2:
                if e.input_2 not in sequences:
                    linked_sequences.append(e.input_2)
        except AttributeError:
            continue

    return linked_sequences

