import os
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
            lines.append(' ' * indent + '"' + key + '": {')
            lines.extend(pretty_json(dictionary[key], indent + 4))
            lines.append(' ' * indent + '}')
        else:
            lines.append(' ' * indent + '"' + key + '": ' + str(dictionary[key]))

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
        json_contents = {}
        for keymap in bpy.context.window_manager.keyconfigs['Blender Addon'].keymaps:
            for keymap_item in keymap.keymap_items:
                if keymap_item.idname.startswith('power_sequencer'):
                    if keymap.name not in json_contents:
                        json_contents[keymap.name] = {}

                    if keymap.space_type not in json_contents[keymap.name]:
                        json_contents[keymap.name][keymap.space_type] = {}

                    if keymap.region_type not in json_contents[keymap.name][keymap.space_type]:
                        json_contents[keymap.name][keymap.space_type][keymap.region_type] = {}

                    json_contents[keymap.name][keymap.space_type][keymap.region_type][keymap_item.idname] = [keymap_item.type, keymap_item.value]

                    if keymap_item.shift:
                        json_contents[keymap.name][keymap.space_type][keymap.region_type][keymap_item.idname].append('SHIFT')
                    if keymap_item.ctrl:
                        json_contents[keymap.name][keymap.space_type][keymap.region_type][keymap_item.idname].append('CTRL')
                    if keymap_item.alt:
                        json_contents[keymap.name][keymap.space_type][keymap.region_type][keymap_item.idname].append('ALT')

        with open(self.filepath, 'w') as f:
            f.write('\n'.join(pretty_json(json_contents)))

        return {"FINISHED"}
