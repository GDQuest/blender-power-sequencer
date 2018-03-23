def is_float(string):
    """
    Determine if a string is a float
    """
    try:
        float(string)
    except ValueError:
        return False
    return True
