import os
import pathlib
import bpy
from bpy_extras.io_utils import ExportHelper
import json


def pretty_json(dictionary, indent=0):
    """
    Makes a pretty string out of a dictionary
    (because I hate the way json.dump does it)
    """
    lines = []

    keys = sorted(list(dictionary.keys()))
    for i in range(len(keys)):
        key = keys[i]
        if type(dictionary[key]) is dict:
            lines.append(' ' * indent + '"' + key + '" : {')
            lines.extend(pretty_json(dictionary[key], indent + 4))
            lines.append(' ' * indent + '}')
        else:
            list_string = '['
            for x in range(len(dictionary[key])):
                item = dictionary[key][x]
                if x < len(dictionary[key]) - 1:
                    list_string += '"' + item + '", '
                else:
                    list_string += '"' + item + '"'
            list_string += ']'
            lines.append(' ' * indent + '"' + key + '" : ' + list_string)

        if not i == len(keys) - 1:
                lines[-1] += ','

    return lines


class ExportKeymap(bpy.types.Operator, ExportHelper):
    """
    Exports Power Sequencer hotkeys to a JSON file
    """
    bl_idname = "power_sequencer.export_keymap"
    bl_label = "Export Keymap"
    bl_desription = "Exports current keymap settings for power-sequencer"

    filename_ext = ".json"

    def execute(self, context):
        self.filepath = os.path.abspath(self.filepath)
        found_op_ids = []
        json_contents = {}
        for keymap in bpy.context.window_manager.keyconfigs['Blender Addon'].keymaps:
            for keymap_item in keymap.keymap_items:
                if keymap_item.idname.startswith('power_sequencer'):
                    if keymap.name not in json_contents.keys():
                        json_contents[keymap.name] = {}

                    if keymap.space_type not in json_contents[keymap.name].keys():
                        json_contents[keymap.name][keymap.space_type] = {}

                    if keymap.region_type not in json_contents[keymap.name][keymap.space_type].keys():
                        json_contents[keymap.name][keymap.space_type][keymap.region_type] = {}

                    json_contents[keymap.name][keymap.space_type][keymap.region_type][keymap_item.idname] = [keymap_item.type, keymap_item.value]

                    if keymap_item.shift:
                        json_contents[keymap.name][keymap.space_type][keymap.region_type][keymap_item.idname].append("SHIFT")
                    if keymap_item.ctrl:
                        json_contents[keymap.name][keymap.space_type][keymap.region_type][keymap_item.idname].append("CTRL")
                    if keymap_item.alt:
                        json_contents[keymap.name][keymap.space_type][keymap.region_type][keymap_item.idname].append("ALT")

                    found_op_ids.append(keymap_item.idname)

        addons_path = bpy.utils.user_resource('SCRIPTS', "addons")
        operators_path = os.path.dirname(__file__)
        folder = pathlib.Path(operators_path.replace(addons_path, '')).parts[1]
        keymap_path = os.path.join(addons_path, folder, 'utils', 'keymap.json')

        with open(keymap_path, 'r') as f:
            orig_keymap = json.load(f)

        names = orig_keymap.keys()
        for name in names:
            space_types = orig_keymap[name].keys()
            for space_type in space_types:
                regions = orig_keymap[name][space_type].keys()
                for region in regions:
                    keymap_items = orig_keymap[name][space_type][region].keys()
                    for kmi in keymap_items:
                        if kmi not in found_op_ids:
                            
                            if name not in json_contents.keys():
                                json_contents[name] = {}

                            if space_type not in json_contents[name].keys():
                                json_contents[name][space_type] = {}

                            if region not in json_contents[name][space_type].keys():
                                json_contents[name][space_type][region] = {}

                            json_contents[name][space_type][region][kmi] = []

        with open(self.filepath, 'w') as f:
            f.write('{\n' + '\n'.join(pretty_json(json_contents, indent=4)) + '\n}')

        return {"FINISHED"}
