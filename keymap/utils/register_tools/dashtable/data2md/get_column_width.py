def get_column_width(column, table):
    """
    Get the character width of a column in a table

    Parameters
    ----------
    column : int
        The column index analyze
    table : list of lists of str
        The table of rows of strings. For this to be accurate, each
        string must only be 1 line long.

    Returns
    -------
        width : int
    """
    width = 3

    for row in range(len(table)):
        cell_width = len(table[row][column])
        if cell_width > width:
            width = cell_width

    return width
