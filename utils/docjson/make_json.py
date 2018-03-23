import os
import json

from .get_operator_tag import get_operator_tag
from .get_operator_shortcuts import get_operator_shortcuts
from .get_operator_docstring import get_operator_docstring
    

def make_json(ops_path, output_path=None):
    """
    Make a JSON out of all the data we gather about the operators
    """
    
    info = {}
    
    for file in sorted(os.listdir(ops_path)):
        if file.endswith('.py') and not file.startswith('_'):
            filepath = os.path.join(ops_path, file)
            
            idname = get_operator_tag(filepath, "bl_idname")
            label = get_operator_tag(filepath, "bl_label")
            description = get_operator_tag(filepath, "bl_description")
            docstring = get_operator_docstring(filepath)
            shortcuts = get_operator_shortcuts(idname)
            
            info[idname] = {}
            info[idname]["label"] = label
            info[idname]["description"] = description
            info[idname]["docstring"] = docstring
            info[idname]["shortcuts"] = shortcuts
    
    if output_path:
        text = json.dumps(info, indent=4, sort_keys=True)
        with open(output_path, 'w') as f:
            f.write(text)
    
    return info
