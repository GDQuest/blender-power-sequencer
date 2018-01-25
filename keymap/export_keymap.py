import os
import bpy
from bpy_extras.io_utils import ExportHelper
import json
from .utils import pretty_json
from .utils import default_keymap


class ExportKeymap(bpy.types.Operator, ExportHelper):
    """
    Exports addon hotkeys to a JSON file
    """
    bl_idname = "power_sequencer.export_keymap"
    bl_label = "Export Keymap"
    bl_desription = "Exports current keymap settings to JSON file"

    filename_ext = ".json"

    def execute(self, context):
        self.filepath = os.path.abspath(self.filepath)
        found_op_ids = []
        json = {}

        kc = bpy.context.window_manager.keyconfigs['Blender Addon']
        for km in kc.keymaps:
            for kmi in km.keymap_items:
                if kmi.idname.startswith('power_sequencer'):
                    name = km.name
                    sp_t = km.space_type
                    re_t = km.region_type
                    id_n = kmi.idname

                    if name not in json.keys():
                        json[name] = {}

                    if sp_t not in json[name].keys():
                        json[name][sp_t] = {}

                    if re_t not in json[name][sp_t].keys():
                        json[name][sp_t][re_t] = {}

                    json[name][sp_t][re_t][id_n] = [kmi.type, kmi.value]

                    if kmi.shift:
                        json[name][sp_t][re_t][id_n].append("SHIFT")
                    if kmi.ctrl:
                        json[name][sp_t][re_t][id_n].append("CTRL")
                    if kmi.alt:
                        json[name][sp_t][re_t][id_n].append("ALT")

                    found_op_ids.append(kmi.idname)

        keymap_filepath = os.path.join(
            os.path.dirname(__file__), 'utils', 'keymap.json')

        try:
            with open(keymap_filepath, 'r') as f:
                user_keymap = json.load(f)
        except FileNotFoundError:
            user_keymap = default_keymap()

        names = user_keymap.keys()
        for name in names:
            space_types = user_keymap[name].keys()
            for sp_t in space_types:
                region_types = user_keymap[name][sp_t].keys()
                for re_t in region_types:
                    keymap_items = user_keymap[name][sp_t][re_t].keys()
                    for kmi in keymap_items:
                        if kmi not in found_op_ids:

                            if name not in json.keys():
                                json[name] = {}

                            if sp_t not in json[name].keys():
                                json[name][sp_t] = {}

                            if re_t not in json[name][sp_t].keys():
                                json[name][sp_t][re_t] = {}

                            json[name][sp_t][re_t][kmi] = []

        with open(self.filepath, 'w') as f:
            f.write(pretty_json(json))

        message = ' '.join(['Exported keymap to',
                            os.path.basename(self.filepath)])
        self.report({'INFO'}, message)

        return {"FINISHED"}