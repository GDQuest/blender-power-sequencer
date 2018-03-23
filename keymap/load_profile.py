import bpy
import os

from .utils import register_keymap
from .utils import unregister_keymap


class LoadProfile(bpy.types.Operator):
    """
    Loads a keymap profile
    """
    bl_idname = "power_sequencer.load_profile"
    bl_label = "Load Keymap"
    bl_desription = "Registers keymap profile"

    def execute(self, context):
        unregister_keymap()

        keymap_path = os.path.join(
            os.path.dirname(__file__), 'utils', 'keymap.json')

        try:
            os.unlink(keymap_path)
        except FileNotFoundError:
            pass

        register_keymap()
        self.report({'INFO'}, 'Loaded keymap')

        return {"FINISHED"}
