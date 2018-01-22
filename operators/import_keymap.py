import os
import pathlib
import shutil
import bpy
from bpy_extras.io_utils import ImportHelper


class ImportKeymap(bpy.types.Operator, ImportHelper):
    """
    Imports Power Sequencer hotkeys from a JSON file
    """
    bl_idname = "power_sequencer.import_keymap"
    bl_label = "Import Keymap"
    bl_desription = "Imports keymap settings from a JSON file"
    
    filter_glob = bpy.props.StringProperty(
            default="*.json",
            options={"HIDDEN"},
            maxlen=255,
            )
    
    def execute(self, context):
        self.filepath = os.path.abspath(self.filepath)
        
        addons_path = bpy.utils.user_resource('SCRIPTS', "addons")
        operators_path = os.path.dirname(__file__)
        folder = pathlib.Path(operators_path.replace(addons_path, '')).parts[1]
        keymap_path = os.path.join(addons_path, folder, 'utils', 'keymap.json')
        
        try:
            os.unlink(keymap_path)
        except FileNotFoundError:
            pass
        
        shutil.copy(self.filepath, keymap_path)
        
        bpy.ops.power_sequencer.unregister_keymap()
        bpy.ops.power_sequencer.register_keymap()
        
        return {"FINISHED"}
