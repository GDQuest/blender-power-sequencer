def add_cushions(table):
    """
    Add space to start and end of each string in a list of lists

    Parameters
    ----------
    table : list of lists of str
        A table of rows of strings. For example::

            [
                ['dog', 'cat', 'bicycle'],
                ['mouse', trumpet', '']
            ]

    Returns
    -------
    table : list of lists of str

    Note
    ----
    Each cell in an rst grid table should to have a cushion of at least
    one space on each side of the string it contains. For example::

        +-----+-------+
        | foo | bar   |
        +-----+-------+
        | cat | steve |
        +-----+-------+

    is better than::

        +-----+---+
        |foo| bar |
        +-----+---+
        |cat|steve|
        +-----+---+
    """
    for row in range(len(table)):
        for column in range(len(table[row])):
            lines = table[row][column].split("\n")

            for i in range(len(lines)):
                if not lines[i] == "":
                    lines[i] = " " + lines[i].rstrip() + " "

            table[row][column] = "\n".join(lines)

    return table
