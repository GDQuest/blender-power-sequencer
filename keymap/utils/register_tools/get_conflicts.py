from .get_current_hotkeys import get_current_hotkeys
from .get_shortcut_string import get_shortcut_string

def get_conflicts(keymap_paths, potential_hotkeys):
    """
    Check through potential_hotkeys and see if any of the shortcuts
    match the current_hotkeys.

    Returns a list of lists:
    [
        [hotkey.idname, potential_hotkey.idname]
    ]
    """
    current_ids = []
    conflicts = [["Current Operation", "Power Sequencer Operation", "Shortcut"]]

    for km_path in keymap_paths:
        group = km_path[0]
        space = km_path[1]
        region = km_path[2]

        hotkeys = get_current_hotkeys(group, space, region)

        shared = [
            'type', 'value', 'any', 'shift', 'ctrl', 'alt', 'oskey',
            'key_modifier']

        for hotkey in hotkeys:
            for kmi in potential_hotkeys:
                if (kmi.group == group and
                        kmi.space_type == space and
                        kmi.region_type == region and
                        hotkey.idname != kmi.idname):

                    same = True
                    for attribute in shared:
                        if not getattr(hotkey, attribute) == getattr(kmi, attribute):
                            same = False

                    if same and hotkey.idname not in current_ids:
                        conflicts.append(
                            [hotkey.idname,
                             kmi.idname,
                             get_shortcut_string(kmi)]
                        )
                        current_ids.append(hotkey.idname)

    return conflicts
