from .get_column_width import get_column_width

from ..dashutils import center_line
from ..dashutils import add_cushions
from ..dashutils import multis_2_mono
from ..dashutils import ensure_table_strings


def data2md(table):
    """
    Creates a markdown table. The first row will be headers.

    Parameters
    ----------
    table : list of lists of str
        A list of rows containing strings. If any of these strings
        consist of multiple lines, they will be converted to single line
        because markdown tables do not support multiline cells.

    Returns
    -------
    str
        The markdown formatted string

    Example
    -------
    >>> table_data = [
    ...     ["Species", "Coolness"],
    ...     ["Dog", "Awesome"],
    ...     ["Cat", "Meh"],
    ... ]
    >>> print(data2md(table_data))
    | Species | Coolness |
    |---------|----------|
    |   Dog   | Awesome  |
    |   Cat   |   Meh    |
    """
    table = ensure_table_strings(table)
    table = multis_2_mono(table)
    table = add_cushions(table)

    widths = []
    for column in range(len(table[0])):
        widths.append(get_column_width(column, table))

    output = '|'
    for i in range(len(table[0])):
        output = ''.join(
            [output, center_line(widths[i], table[0][i]), '|'])

    output = output + '\n|'
    for i in range(len(table[0])):
        output = ''.join([
            output, center_line(widths[i], "-" * widths[i]), '|'])
    output = output + '\n|'

    for row in range(1, len(table)):
        for column in range(len(table[row])):
            output = ''.join(
                [output, center_line(widths[column],
                 table[row][column]), '|'])
        output = output + '\n|'

    split = output.split('\n')
    split.pop()

    table_string = '\n'.join(split)

    return table_string
