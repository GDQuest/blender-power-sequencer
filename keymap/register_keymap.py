import os
import bpy
from .utils import func_register_keymap

class RegisterKeymap(bpy.types.Operator):
    """
    Create an operator for the register keymap function
    """
    bl_idname = "power_sequencer.register_keymap"
    bl_label = "Register keymap"
    bl_description = "Registers addon keymap"
    
    def execute(self, context):
        func_register_keymap()
        
        return {"FINISHED"}
