from .dashtable import data2md
from .dashtable import center_line


def print_conflicts(conflicts):
    """
    Output to console a list of hotkeys that will be overridden

    Parameters
    ----------
    conflicts : list of lists
        For example: [ [current shortcut ID] [new shortcut ID] [hotkey] ]
    """

    conflict_string = data2md(conflicts)

    first_line = conflict_string.split('\n')[0]
    title = center_line(
        len(first_line), "Shortcuts Overridden by VSE_Transform_Tools")
    underline = center_line(len(first_line), '=' * len(title.strip()))

    if (len(conflicts)) > 1:
        print('\n'.join(['', title, underline, conflict_string, '']))
