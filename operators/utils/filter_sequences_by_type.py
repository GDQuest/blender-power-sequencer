def filter_sequences_by_type(sequences, *args):
    """
    Takes a list of sequences and returns a list of sequences with types
    that correspond to the types passed in args.
    Use the SequenceTypes class for the args

    Args:
    - sequences: a list of sequences
    - args: any list of sequence types. i.e. SequenceTypes.VIDEO
    """
    types_list = []
    for arg in args:
        if not isinstance(arg, list):
            raise TypeError('An argument is not a list')
    for arg in args:
        types_list.extend(arg)

    return [s for s in sequences if s.type in types_list]
