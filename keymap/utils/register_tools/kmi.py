from .is_int import is_int
from .is_float import is_float


class KMI():
    """
    A simple class for holding keymap_item information

    This attempts to be a copy of bpy.types.KeyMapItem, except for
    some changes in the defaults.
    """
    # See the following for options on space_type, region, window:
    # https://docs.blender.org/api/blender_python_api_2_78_release/bpy.types.KeyMaps.html
    group = "Sequencer"
    space_type = "SEQUENCE_EDITOR"
    region_type = "WINDOW"

    # These values based on:
    # https://docs.blender.org/api/blender_python_api_2_77_0/bpy.types.KeyMapItems.html#bpy.types.KeyMapItems.new
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

    def __init__(self, idname, hotkey_list):
        self.idname = idname

        for item in hotkey_list:
            if not item.startswith("properties"):
                attribute = item.split('=')[0].strip()
                value = item.split('=')[1].strip()
                if is_int(value):
                    value = int(value)
                elif is_float(value):
                    value = float(value)
                elif value == "True":
                    value = True
                elif value == "False":
                    value = False

                setattr(self, attribute, value)
            else:
                properties = {}
                pairs = item.replace('properties', '').strip()[1::].split(';')
                for pair in pairs:
                    attribute = pair.split(':')[0].strip()
                    value = pair.split(':')[1].strip()
                    if is_int(value):
                        value = int(value)
                    elif is_float(value):
                        value = float(value)
                    elif value == "True":
                        value = True
                    elif value == "False":
                        value = False

                    if not attribute == "":
                        properties[attribute] = value

                self.properties = dict(properties)
