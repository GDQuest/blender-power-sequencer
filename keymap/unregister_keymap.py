import os
import bpy
from .utils import func_unregister_keymap


class UnregisterKeymap(bpy.types.Operator):
    """
    Operator for the unregister keymap function
    """
    bl_idname = "power_sequencer.unregister_keymap"
    bl_label = "Unregister keymap"
    bl_description = "Unregisters keymap"

    def execute(self, context):
        
        func_unregister_keymap()
        return {"FINISHED"}
