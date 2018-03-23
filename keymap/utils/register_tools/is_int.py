def is_int(string):
    """
    Determine if a string is an integer
    """
    try:
        int(string)
    except ValueError:
        return False
    return True
