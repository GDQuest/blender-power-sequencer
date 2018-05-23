import os
import pathlib
import bpy


def get_addon_module_name():
    """
    Gets the name of the base folder housing this addon
    """
    addons_path = bpy.utils.user_resource('SCRIPTS', "addons")
    module_path = os.path.dirname(__file__)

    cleaned = module_path.replace(addons_path, '')

    purepath = pathlib.PurePath(cleaned)

    return purepath.parts[1]
