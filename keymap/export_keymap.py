import os
import bpy
from bpy_extras.io_utils import ExportHelper
from .utils import pretty_json


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
                if kmi.idname.startswith('power_sequencer') and kmi.active:
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

                    if id_n not in json[name][sp_t][re_t].keys():
                        json[name][sp_t][re_t][id_n] = {}

                    key = str(len(json[name][sp_t][re_t][id_n]))
                    hotkey_list = json[name][sp_t][re_t][id_n][key] = []

                    hotkey_list.append("type=" + kmi.type)

                    if not kmi.value == "PRESS":
                        hotkey_list.append("value=" + kmi.value)
                    if kmi.alt:
                        hotkey_list.append("alt=" + str(kmi.alt))
                    if kmi.any:
                        hotkey_list.append("any=" + str(kmi.any))
                    if kmi.shift:
                        hotkey_list.append("shift=" + str(kmi.shift))
                    if kmi.ctrl:
                        hotkey_list.append("ctrl=" + str(kmi.ctrl))
                    if kmi.key_modifier != "NONE":
                        hotkey_list.append("key_modifier=" + kmi.key_modifier)
                    if kmi.oskey:
                        hotkey_list.append("oskey=" + str(kmi.oskey))

                    if len(kmi.properties.items()) > 0:
                        properties = []
                        for key in kmi.properties.keys():
                            value = getattr(kmi.properties, key)
                            properties.append(''.join([key, ':', str(value)]))

                        prop_str = "properties=" + ';'.join(properties)
                        hotkey_list.append(prop_str)

                    found_op_ids.append(kmi.idname)

        with open(self.filepath, 'w') as f:
            f.write(pretty_json(json))

        message = ' '.join(['Exported keymap to',
                            os.path.basename(self.filepath)])
        self.report({'INFO'}, message)

        return {"FINISHED"}
