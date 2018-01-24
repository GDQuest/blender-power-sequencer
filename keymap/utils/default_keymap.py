# Available keys found at:
# https://docs.blender.org/api/2.78/bpy.types.KeyMapItem.html

def default_keymap():
    """
    Defines the default keymap
    """
    
    default_keymap = {
        "Sequencer": {
            "SEQUENCE_EDITOR" : {
                "WINDOW": {
                    "power_sequencer.concatenate_strips" : [],
                    "power_sequencer.mouse_cut": ["ACTIONMOUSE", "PRESS", "CTRL"],
                    "power_sequencer.ripple_delete": ["X", "PRESS", "SHIFT"]
                }
            }
        }
    }
    
    return default_keymap
