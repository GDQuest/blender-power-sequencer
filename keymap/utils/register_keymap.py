import os
import json
import bpy
from .default_keymap import default_keymap

# For more info on keymaps see:
# https://docs.blender.org/api/blender_python_api_2_78_release/bpy.types.KeyMaps.html


def register_keymap():
    """
    Use the keymap.json file to create hotkeys.

    Will overwrite existing hotkeys if conflicting, but prints these
    to console.
    """

    keymap_filepath = os.path.join(
        os.path.dirname(__file__), 'keymap.json')

    try:
        with open(keymap_filepath, 'r') as f:
            keymap_data = json.load(f)
    except FileNotFoundError:
        keymap_data = default_keymap()

    keymap_names = keymap_data.keys()
    for name in keymap_names:
        space_types = keymap_data[name].keys()

        for space_type in space_types:
            region_types = keymap_data[name][space_type].keys()

            for region in region_types:
                operator_names = keymap_data[name][space_type][region].keys()

                keyconfig = bpy.context.window_manager.keyconfigs[
                    'Blender Addon']
                keymap = keyconfig.keymaps.new(
                    name, space_type=space_type, region_type=region)

                current_hotkeys = []
                default_keyconfig_names = [
                    'Blender', 'Blender Addon', 'Blender User']
                for def_kc in default_keyconfig_names:
                    try:
                        kc = bpy.context.window_manager.keyconfigs[def_kc]
                        current_hotkeys.extend(
                            kc.keymaps[name].keymap_items)
                    except KeyError:
                        pass

                for op in operator_names:
                    numbers = keymap_data[name][space_type][region][op].keys()
                    for number in numbers:
                        shortcut = keymap_data[name][space_type][region][op][number]
                        if len(shortcut) > 0:
                            shift = 'SHIFT' in shortcut
                            alt = 'ALT' in shortcut
                            ctrl = 'CTRL' in shortcut

                            status = "PRESS"
                            other_status_types = [
                                "ANY", "NOTHING", "RELEASE", "CLICK",
                                "DOUBLE_CLICK", "NORTH", "NORTH_EAST",
                                "EAST", "SOUTH_EAST", "SOUTH",
                                "SOUTH_WEST", "WEST", "NORTH_WEST"]

                            for status_type in other_status_types:
                                if status_type in shortcut:
                                    status = status_type
                                    break

                            for hotkey in current_hotkeys:
                                if (not hotkey.idname == op and
                                   hotkey.type == shortcut[0] and
                                   hotkey.value == status and
                                   hotkey.shift == shift and
                                   hotkey.ctrl == ctrl and
                                   hotkey.alt == alt):
                                    print(' '.join(['Conflicting hotkeys:',
                                                    hotkey.idname,
                                                    'vs',
                                                    op,
                                                    '...OVERWRITING']))

                            try:
                                kmi = keymap.keymap_items.new(
                                    op,
                                    shortcut[0],
                                    status,
                                    shift=shift, alt=alt, ctrl=ctrl)

                            # User tried an invalid key name
                            except TypeError:
                                print(' '.join([
                                        'Error:',
                                        'Unable to make keyboard shortcut for',
                                        op]))