import os
import json
import bpy
from .keymap_profiles import *
from .pretty_json import pretty_json
from .get_addon_module_name import get_addon_module_name
from .data2md import data2md, centerWord

# For more info on keymaps see:
# https://docs.blender.org/api/blender_python_api_2_78_release/bpy.types.KeyMaps.html


def kmi_props_setattr(kmi_props, attr, value):
    try:
        setattr(kmi_props, attr, value)
    except AttributeError:
        print("Warning: property '%s' not found in keymap item '%s'" %
              (attr, kmi_props.__class__.__name__))
    except Exception as e:
        print("Warning: %r" % e)


class KMI():
    """
    A simple class for holding keymap_item information

    This attempts to be a copy of bpy.types.KeyMapItem, except for
    some changes in the defaults.
    """
    # See the following for options on space_type, region, window:
    # https://docs.blender.org/api/blender_python_api_2_78_release/bpy.types.KeyMaps.html
    group = "Sequencer"
    space_type = "SEQUENCE_EDITOR"
    region_type = "WINDOW"

    # These values based on:
    # https://docs.blender.org/api/blender_python_api_2_77_0/bpy.types.KeyMapItems.html#bpy.types.KeyMapItems.new
    idname = ""
    type = "NONE"
    value = "PRESS"
    any = False
    shift = False
    ctrl = False
    alt = False
    oskey = False
    key_modifier = "NONE"
    head = False

    properties = {}

    def __init__(self, idname, hotkey_list):
        self.idname = idname

        for item in hotkey_list:
            if not item.startswith("properties"):
                attribute = item.split('=')[0].strip()
                value = item.split('=')[1].strip()
                if is_int(value):
                    value = int(value)
                elif is_float(value):
                    value = float(value)
                elif value == "True":
                    value = True
                elif value == "False":
                    value = False

                setattr(self, attribute, value)
            else:
                properties = {}
                pairs = item.replace('properties', '').strip()[1::].split(';')
                for pair in pairs:
                    attribute = pair.split(':')[0].strip()
                    value = pair.split(':')[1].strip()
                    if is_int(value):
                        value = int(value)
                    elif is_float(value):
                        value = float(value)
                    elif value == "True":
                        value = True
                    elif value == "False":
                        value = False

                    if not attribute == "":
                        properties[attribute] = value

                self.properties = dict(properties)


def is_int(string):
    """
    Determine if a string is an integer
    """
    try:
        int(string)
    except ValueError:
        return False
    return True


def is_float(string):
    """
    Determine if a string is a float
    """
    try:
        float(string)
    except ValueError:
        return False
    return True


def get_current_hotkeys(group, space, region):
    """
    Collect all current Blender hotkeys in a group with matching space
    and region.

    Group names can be found in Blender > User Preferences > Input
    """
    hotkeys = []
    keyconfig_names = ['Blender', 'Blender Addon', 'Blender User']

    for kc_name in keyconfig_names:
        try:
            kc = bpy.context.window_manager.keyconfigs[kc_name]
            km = kc.keymaps[group]
            if km.space_type == space and km.region_type == region:
                hotkeys.extend(km.keymap_items)
        except KeyError:
            pass
    return hotkeys


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
        addon_name = get_addon_module_name()
        preferences = bpy.context.user_preferences.addons[addon_name].preferences
        profile = preferences.keymap_profile
        keymap_data = globals()[profile]()

    keymap_paths, potential_hotkeys = get_potential_hotkeys(keymap_data)

    conflicts = get_conflicts(keymap_paths, potential_hotkeys)
    conflict_string = data2md(conflicts)

    first_line = conflict_string.split('\n')[0]
    title = centerWord(len(first_line), "Shortcuts Overridden by Power Sequencer")
    underline = centerWord(len(first_line), "=" * len(title.strip()))

    if len(conflicts) > 0:
        print('\n'.join(['', title, underline, conflict_string, '']))

    keyconfig = bpy.context.window_manager.keyconfigs.addon
    if not keyconfig:
        keyconfig = bpy.context.window_manager.keyconfigs.new("Blender Addon")
    for keymap_path in keymap_paths:
        group = keymap_path[0]
        space = keymap_path[1]
        region = keymap_path[2]

        try:
            km = keyconfig.keymaps[group]
        except KeyError:
            km = keyconfig.keymaps.new(
                group, space_type=space, region_type=region)

        for kmi in potential_hotkeys:
            new_keymap_item = km.keymap_items.new(
                kmi.idname, kmi.type, kmi.value,
                any=kmi.any, shift=kmi.shift, ctrl=kmi.ctrl, alt=kmi.alt,
                oskey=kmi.oskey, key_modifier=kmi.key_modifier,
                head=kmi.head)

            for attribute in kmi.properties.keys():
                value = kmi.properties[attribute]
                kmi_props_setattr(new_keymap_item.properties, attribute, value)
