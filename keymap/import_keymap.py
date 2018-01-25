import os
import shutil
import bpy
from bpy_extras.io_utils import ImportHelper
import json
from .utils import unregister_keymap
from .utils import register_keymap

class ImportKeymap(bpy.types.Operator, ImportHelper):
    """
    Set addon hotkeys based on a JSON file
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

        try:
            with open(self.filepath, 'r') as f:
                json.load(f)
        except json.decoder.JSONDecodeError:
            message = '\n'.join([
                'User provided .json file is not formatted correctly',
                'No Keymaps were changed.'])

            self.report({'ERROR'}, message)
            return {"FINISHED"}

        unregister_keymap()

        keymap_path = os.path.join(
            os.path.dirname(__file__), 'utils', 'keymap.json')

        try:
            os.unlink(keymap_path)
        except FileNotFoundError:
            pass

        shutil.copy(self.filepath, keymap_path)

        register_keymap()
        self.report({'INFO'}, 'Keymap updated')

        return {"FINISHED"}