from .kmi import KMI


def get_potential_hotkeys(keymap_data):
    """
    Use keymap_data dictionary to create a list of potential hotkeys
    to add to Blender.
    """
    keymap_paths = []
    potential_hotkeys = []

    for group in keymap_data.keys():
        space_types = keymap_data[group].keys()
        for space in space_types:
            region_types = keymap_data[group][space].keys()
            for region in region_types:
                operator_names = keymap_data[group][space][region].keys()
                for op in operator_names:
                    numbers = keymap_data[group][space][region][op].keys()
                    for number in numbers:
                        hotkey_list = keymap_data[group][space][region][op][number]
                        if len(hotkey_list) > 0:
                            kmi = KMI(op, hotkey_list)
                            potential_hotkeys.append(kmi)
                            if not [group, space, region] in keymap_paths:
                                keymap_paths.append([group, space, region])

    return keymap_paths, potential_hotkeys
