'''
Copyright (C) 2016-2018 Nathan Lovato, Davide Cristi
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
    "description": "Video editing tools for content creators",
    "author": "Nathan Lovato",
    "version": (0, 9, 0),
    "blender": (2, 79, 0),
    "location": "sequencer",
    "warning": "Beta release, may contain bugs",
    "wiki_url": "https://www.youtube.com/playlist?list=PLhqJJNjsQ7KFjp88Cu57Zb9_wFt7nlkEI",
    "support": "COMMUNITY",
    "category": "VSE"
}

import bpy
import os
from math import ceil
from operator import attrgetter
from enum import Enum
from .handlers import handlers_register, handlers_unregister

from . import addon_updater_ops

# load and reload submodules
##################################
from .utils import developer_utils
modules = developer_utils.setup_addon_modules(__path__, __name__)

# register
##################################
import traceback

from .operators import *
from .keymap import *

from .keymap.utils import register_keymap
from .keymap.utils import unregister_keymap

class PowerSequencerProperties(bpy.types.PropertyGroup):
    playback_speed = bpy.props.EnumProperty(
        items=[('normal', 'Normal (1x)', ''), ('fast', 'Fast (1.33x)', ''),
               ('faster', 'Faster (1.66x)', ''), ('double', 'Double (2x)', ''),
               ('triple', 'Triple (3x)', '')],
        name='Playback speed',
        default='normal')

    frame_pre = bpy.props.IntProperty(
        name='Frame before frame_change', default=0, min=0)

    active_tab = bpy.props.StringProperty(
        name="Active Tab",
        description="The name of the active tab in the UI",
        default="Sequencer"
        )


def register():
    addon_updater_ops.register(bl_info)

    try:
        bpy.utils.register_module(__name__)
    except:
        traceback.print_exc()

    bpy.types.Scene.power_sequencer = bpy.props.PointerProperty(
        type=PowerSequencerProperties)

    handlers_register()

    print("Registered {} with {} modules".format(bl_info["name"], len(
        modules)))

    register_keymap()


def unregister():
    unregister_keymap()

    try:
        bpy.utils.unregister_module(__name__)
    except:
        traceback.print_exc()

    handlers_unregister()
    print("Unregistered {}".format(bl_info["name"]))
