# This module from dashtable by doakey3
# https://github.com/doakey3/DashTable
import math


def lineBreak(count, symbol):
    """makes a string that is count long of symbol"""
    x = ""
    for i in range(0, count):
        x = x + symbol
    return x


def centerWord(space, line):
    """Centers text to available space"""
    left = math.floor((space - len(line)) / 2)
    right = math.ceil((space - len(line)) / 2)

    left_space = lineBreak(left, ' ')
    right_space = lineBreak(right, ' ')

    line = left_space + line + right_space
    return line


def getColumnWidth(column, table):
    width = 3
    for r in range(len(table)):
        w = len(table[r][column])
        if w > width:
            width = w
    return width


def removeNewlines(table):
    """
    Replaces newlines with ' '
    """
    for r in range(len(table)):
        for c in range(len(table[r])):
            table[r][c] = table[r][c].replace('\n', ' ')
    return table


def addCushions(table):
    """adds space to start and end of each item in a list of lists"""
    for row in range(len(table)):
        for column in range(len(table[row])):
            lines = table[row][column].split("\n")
            for i in range(len(lines)):
                if not lines[i] == "":
                    lines[i] = " " + lines[i].rstrip() + " "
            table[row][column] = "\n".join(lines)
    return table


def data2md(table):
    """
    Creates a table in the markdown table format
    """

    for row in range(len(table)):
        for column in range(len(table[row])):
            table[row][column] = str(table[row][column])

    table = removeNewlines(table)
    table = addCushions(table)

    widths = []
    for c in range(len(table[0])):
        widths.append(getColumnWidth(c, table))

    output = '|'
    for i in range(len(table[0])):
        output = output + centerWord(widths[i], table[0][i]) + '|'
    output = output + '\n|'
    for i in range(len(table[0])):
        output = ''.join([output, centerWord(widths[i],
                          lineBreak(widths[i], '-')), '|'])
    output = output + '\n|'

    for r in range(1, len(table)):
        for c in range(len(table[r])):
            output = output + centerWord(widths[c], table[r][c]) + '|'
        output = output + '\n|'

    split = output.split('\n')
    split.pop()

    return '\n'.join(split)
