def multis_2_mono(table):
    """
    Converts each multiline string in a table to single line.

    Parameters
    ----------
    table : list of list of str
        A list of rows containing strings

    Returns
    -------
    table : list of lists of str
    """
    for row in range(len(table)):
        for column in range(len(table[row])):
            table[row][column] = table[row][column].replace('\n', ' ')

    return table
