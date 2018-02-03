def get_shortcut_string(kmi):
    """
    Get the keyboard shortcut for a keymap item in an easy-to-read
    string
    """

    shortcut_string = []
    if kmi.ctrl:
        shortcut_string.append('Ctrl')
    if kmi.alt:
        shortcut_string.append('Alt')
    if kmi.shift:
        shortcut_string.append('Shift')
    if kmi.oskey:
        shortcut_string.append('OSKey')
    if kmi.any:
        shortcut_string.append('Any')
    if kmi.key_modifier != "NONE":
        shortcut_string.append(kmi.key_modifier)

    shortcut_string.append(kmi.type)

    return ' '.join(shortcut_string)
