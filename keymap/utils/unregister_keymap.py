import os
import json
import bpy
from .keymap_profiles import *
from .get_addon_module_name import get_addon_module_name


def unregister_keymap():
    """
    Remove keymaps
    """

    keymap_filepath = os.path.join(
        os.path.dirname(__file__), 'keymap.json')

    try:
        with open(keymap_filepath, 'r') as f:
            keymap_data = json.load(f)
    except FileNotFoundError:
        addon_name = get_addon_module_name()
        preferences = bpy.context.user_preferences.addons[addon_name].preferences
        profile = preferences.keymap_profile
        keymap_data = globals()[profile]()

    keymap_names = keymap_data.keys()
    for name in keymap_names:
        space_types = keymap_data[name].keys()
        for space_type in space_types:
            region_types = keymap_data[name][space_type].keys()
            for region in region_types:
                operator_names = keymap_data[name][space_type][region].keys()

                kc = bpy.context.window_manager.keyconfigs.addon
                keymap = kc.keymaps.new(
                    name, space_type=space_type, region_type=region)
                current_hotkeys = keymap.keymap_items

                for hotkey in current_hotkeys:
                    if hotkey.idname in operator_names:
                        keymap.keymap_items.remove(hotkey)

    keymap_path = os.path.join(
            os.path.dirname(__file__), 'keymap.json')

    try:
        os.unlink(keymap_path)
    except FileNotFoundError:
        pass
