import os
import json
import bpy

# For more info on keymaps see:
# https://docs.blender.org/api/blender_python_api_2_78_release/bpy.types.KeyMaps.html


def register_keymap():
    """
    Use the keymap.json file to create hotkeys for power sequencer.

    Will overwrite existing hotkeys if conflicting, but prints these
    to console.
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
                    if len(operators[op]) > 0:
                        shift = 'SHIFT' in operators[op]
                        alt = 'ALT' in operators[op]
                        ctrl = 'CTRL' in operators[op]

                        for hotkey in current_hotkeys:
                            if (not hotkey.idname == op and
                               hotkey.type == operators[op][0] and
                               hotkey.value == operators[op][1] and
                               hotkey.shift == shift and
                               hotkey.ctrl == ctrl and
                               hotkey.alt == alt):
                                print(' '.join(['Conflicting hotkeys:',
                                                hotkey.idname,
                                                'vs',
                                                op,
                                                '... OVERWRITING']))
                        try:
                            kmi = keymap.keymap_items.new(
                                op,
                                operators[op][0],
                                operators[op][1],
                                shift=shift, alt=alt, ctrl=ctrl)

                        # User tried an invalid key name
                        except TypeError:
                            print(' '.join([
                                    'Error:',
                                    'Unable to make keyboard shortcut for',
                                    op]))

class RegisterKeymap(bpy.types.Operator):
    """
    Use the keymap.json file to create hotkeys for power sequencer.
    """
    bl_idname = "power_sequencer.register_keymap"
    bl_label = "Register Power-Sequencer Keymap"
    bl_description = "Registers Power-Sequencer keymap"
    
    def execute(self, context):
        register_keymap()
        return {"FINISHED"}
        
