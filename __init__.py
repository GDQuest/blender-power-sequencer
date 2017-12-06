'''
Copyright (C) 2016 Nathan Lovato
nathan@gdquest.com

Created by Nathan Lovato

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Power Sequencer",
    "description": "Tools for an efficient video editing workflow",
    "author": "Nathan Lovato",
    "version": (0, 4, 0),
    "blender": (2, 78, 0),
    "location": "sequencer",
    "warning": "This is a Work In Progress",
    "wiki_url": "https://github.com/GDquest/Blender-power-sequencer",
    "support": "COMMUNITY",
    "category": "VSE"
}

import bpy
import os
from math import ceil
from operator import attrgetter
from enum import Enum
from .handlers import handlers_register, handlers_unregister, PowerSequencerProps

# load and reload submodules
##################################
from .functions import developer_utils
modules = developer_utils.setup_addon_modules(__path__, __name__)

# register
##################################
import traceback


def register():
    try:
        bpy.utils.register_module(__name__)
    except:
        traceback.print_exc()

    # Store properties access in the scene and store initial frame
    bpy.types.Scene.power_sequencer = bpy.props.PointerProperty(type=PowerSequencerProps)
    handlers_register()

    print("Registered {} with {} modules".format(bl_info["name"], len(
        modules)))


def unregister():
    try:
        bpy.utils.unregister_module(__name__)
    except:
        traceback.print_exc()

    handlers_unregister()

    print("Unregistered {}".format(bl_info["name"]))
