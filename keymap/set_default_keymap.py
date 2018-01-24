import bpy
import os

from .utils import func_register_keymap
from .utils import func_unregister_keymap

class SetDefaultKeymap(bpy.types.Operator):
    """
    Reset Power-Sequencer keymap to default
    """
    bl_idname = "power_sequencer.set_default_keymap"
    bl_label = "Set default keymap"
    bl_desription = "Removes user keymap file and re-registers hotkeys"

    def execute(self, context):
        func_unregister_keymap()
        
        keymap_path = os.path.join(
            os.path.dirname(__file__), 'utils', 'keymap.json')
        
        try:
            os.unlink(keymap_path)
        except FileNotFoundError:
            pass
        
        func_register_keymap()
        self.report({'INFO'}, 'Applied default keymap')
            
        return {"FINISHED"}
