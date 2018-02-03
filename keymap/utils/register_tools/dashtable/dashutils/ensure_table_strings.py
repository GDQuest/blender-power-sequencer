def ensure_table_strings(table):
    """
    Force each cell in the table to be a string

    Parameters
    ----------
    table : list of lists

    Returns
    -------
    table : list of lists of str
    """
    for row in range(len(table)):
        for column in range(len(table[row])):
            table[row][column] = str(table[row][column])
    return table
