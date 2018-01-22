import os
import json
import bpy


def unregister_keymap():
    """
    Remove keymaps for Power-Sequencer
    """
    keymap_filepath = os.path.join(
        os.path.dirname(__file__), 'keymap.json')

    with open(keymap_filepath, 'r') as f:
        keymap_data = json.load(f)
        
    keymap_names = keymap_data.keys()
    for name in keymap_names:
        space_types = keymap_data[name].keys()
        for space_type in space_types:
            region_types = keymap_data[name][space_type].keys()
            for region in region_types:
                operators = keymap_data[name][space_type][region]
                operator_names = operators.keys()
                
                keyconfig = bpy.context.window_manager.keyconfigs['Blender Addon']
                keymap = keyconfig.keymaps.new(
                    name, space_type=space_type, region_type=region)
                current_hotkeys = keymap.keymap_items
                for hotkey in current_hotkeys:
                    if hotkey.idname in operator_names:
                        keymap.keymap_items.remove(hotkey)


class UnregisterKeymap(bpy.types.Operator):
    """
    Remove keymaps for Power-Sequencer
    """
    bl_idname = "power_sequencer.unregister_keymap"
    bl_label = "Unregister Power-Sequencer Keymap"
    bl_description = "Unregisters Power-Sequencer keymap"

    def execute(self, context):
        unregister_keymap()
        return {"FINISHED"}
