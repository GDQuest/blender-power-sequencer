import os
import sys

default_keymap_folder_path = os.path.join(os.path.dirname(__file__),
                                          "../", "../", "keymap", 
                                          "utils", "keymap_profiles")
sys.path.append(default_keymap_folder_path)
from default import default

def hotkey_list_2_str(keylist):
    """
    converts hotkey list to nice, readable list of strings
    """
    strings = []
    
    if "ctrl=True" in keylist:
        strings.append("Ctrl")
    if "alt=True" in keylist:
        strings.append("Alt")
    if "shift=True" in keylist:
        strings.append("Shift")
    if "oskey=True" in keylist:
        strings.append("OSKey")
    if "any=True" in keylist:
        strings.append("Any")
    
    for item in keylist:
        if item.startswith("key_modifier=") and not item == "key_modifier=NONE":
            strings.append(item.replace("key_modifier=", ""))
            break
    
    for item in keylist:
        if item.startswith("type="):
            strings.append(item.replace("type=", ""))
            break
    return strings

def get_operator_shortcuts(idname):
    """
    Use the keymap_path (ie: default.py) to get an operator's
    keyboard shortcuts
    """
    shortcuts = {}
    
    json = default()
    for group in json.keys():
        for space in json[group].keys():
            for region in json[group][space].keys():
                for op in json[group][space][region].keys():
                    if op == idname:
                        for key in json[group][space][region][op].keys():
                            shortcuts[key] = "keys=" + ', '.join(hotkey_list_2_str(json[group][space][region][op][key]))
                            for item in json[group][space][region][op][key]:
                                if item.startswith('properties='):
                                    props = item.replace('properties=', '').split(';')
                                    for prop in props:
                                        if prop.split(':')[0].strip() == 'function':
                                            shortcuts[key] += "; function=" + prop.split(':')[1].strip()
                                            break
                                    break
    return shortcuts
