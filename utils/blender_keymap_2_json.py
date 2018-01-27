# This is a rough script for converting blender keymaps to a JSON that power-sequencer can import

class KMI():
    """
    A simple class for holding keymap_item information
    """
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
    
    def to_hotkey_list(self):
        hotkey_list = []
        
        hotkey_list.append("type=" + self.type)

        if not self.value == "PRESS":
            hotkey_list.append("value=" + self.value)
        if self.alt:
            hotkey_list.append("alt=" + str(self.alt))
        if self.any:
            hotkey_list.append("any=" + str(self.any))
        if self.shift:
            hotkey_list.append("shift=" + str(self.shift))
        if self.ctrl:
            hotkey_list.append("ctrl=" + str(self.ctrl))
        if self.key_modifier != "NONE":
            hotkey_list.append("key_modifier=" + self.key_modifier)
        if self.oskey:
            hotkey_list.append("oskey=" + str(self.oskey))

        if len(self.properties.keys()) > 0:
            properties = []
            for key in self.properties.keys():
                value = self.properties[key]
                properties.append(''.join([key, ':', str(value)]))

            prop_str = "properties=" + '; '.join(properties)
            hotkey_list.append(prop_str)
        
        return hotkey_list
            


def indent_json(dictionary, indent=0):
    """
    Makes an indented json string out of a dictionary,
    but non dictionary elements are not indented.
    """
    lines = []

    keys = sorted(list(dictionary.keys()))
    for i in range(len(keys)):
        key = keys[i]
        if type(dictionary[key]) is dict:
            lines.append(' ' * indent + '"' + key + '" : {')
            lines.extend(indent_json(dictionary[key], indent + 4))
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


def pretty_json(dictionary):
    """
    Make a json file that is reader-friendly
    """
    output = ['{', '\n'.join(indent_json(dictionary, indent=4)), '}']
    return '\n'.join(output)


def parse_km(line):
    """
    Get the important parts from a line starting with 'km = '
    """
    group = line.split('(')[1][1::].split(',')[0].replace("'", "").replace(")", "")
    space_type = line.split('space_type=')[1][1::].split(',')[0].replace("'", "").replace(")", "")
    region_type = line.split('region_type=')[1][1::].split(',')[0].replace("'", "").replace(")", "")
    
    return group, space_type, region_type


def parse_kmi(line):
    """
    Get the important parts from a line starting with kmi = 
    """
    kmi = KMI()
    
    kmi.idname = line.split('(')[1].split(',')[0].replace("'", "").replace(")", "")
    kmi.type = line.split(',')[1].strip().replace("'", "").replace(")", "")
    kmi.value = line.split(',')[2].strip().replace("'", "").replace(")", "")
    
    if "alt=True" in line:
        kmi.alt = "True"
    if "any=True" in line:
        kmi.any = "True"
    if "shift=True" in line:
        kmi.shift = "True"
    if "ctrl=True" in line:
        kmi.ctrl = "True"
    if "key_modifier" in line:
        kmi.key_modifier = line.split('key_modifier=')[1].split(',')[0].replace("'", "").replace(")", "")
    if "oskey" in line:
        kmi.oskey = "True"
    
    return kmi

def parse_kmi_props(line, kmi):
    """
    Parse the properties in a line that starts with "kmi_props"
    Add the properties to the kmi object
    """
    attribute = line.split(',')[1].strip().replace("'", "")
    value = line.split(',')[-1].strip().replace("'", "").replace(')', '')
    kmi.properties[attribute] = value

def remove_spaces(lines):
    """
    remove the empty lines
    """
    i = 0
    while i < len(lines):
        if lines[i].rstrip() == '':
            lines.pop(i)
        else:
            i += 1
    return lines

def parse_keymap(filepath):
    """
    parse a python keymap into a json
    """
    with open(filepath, 'r') as f:
        lines = f.read().strip().split('\n')
    
    lines = remove_spaces(lines)
    
    json = {}
    
    i = 0
    while i < len(lines):
        if lines[i].startswith('km = '):
            group, space, region = parse_km(lines[i])
            if not group in json.keys():
                json[group] = {}
            
            if not space in json[group].keys():
                json[group][space] = {}
            
            if not region in json[group][space].keys():
                json[group][space][region] = {}
            
            i += 1
            while i < len(lines) and lines[i].startswith('kmi ='):
                kmi = parse_kmi(lines[i])
                kmi.properties = {}
                i += 1
                while i < len(lines) and lines[i].startswith('kmi_props'):
                    parse_kmi_props(lines[i], kmi)
                    i += 1
                
                if not kmi.idname in json[group][space][region].keys():
                    json[group][space][region][kmi.idname] = {}
                
                key = str(len(json[group][space][region][kmi.idname].keys()))
                json[group][space][region][kmi.idname][key] = kmi.to_hotkey_list()
        else:
            i += 1
    
    return pretty_json(json)

if __name__ == "__main__":
    
    keymap_filepath = "Premiere_Keyboard_Layout.py"
    output_filepath = "output.json"
    
    string = parse_keymap(keymap_filepath)
    
    with open(output_filepath, 'w') as f:
        f.write(string)
                
                
                    
                

