'''
Copyright (C) 2016-2018 Nathan Lovato, Davide Cristi, Daniel Oakey, Patrick W. Crawford
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
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "sequencer",
    "tracker_url": "https://github.com/GDquest/Blender-power-sequencer/issues",
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


def kmi_props_setattr(kmi_props, attr, value):
    try:
        setattr(kmi_props, attr, value)
    except AttributeError:
        print("Warning: property '%s' not found in keymap item '%s'" %
              (attr, kmi_props.__class__.__name__))
    except Exception as e:
        print("Warning: %r" % e)


addon_keymaps = []


def register():
    addon_updater_ops.register(bl_info)

    try:
        bpy.utils.register_module(__name__)
    except:
        traceback.print_exc()

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(
        name='Sequencer',
        space_type='SEQUENCE_EDITOR',
        region_type='WINDOW')

    kmi = km.keymap_items.new('power_sequencer.add_crossfade', 'C', 'PRESS', ctrl=True, alt=True)
    kmi = km.keymap_items.new('power_sequencer.add_speed', 'PLUS', 'PRESS', shift=True)
    kmi = km.keymap_items.new('power_sequencer.add_transform', 'T', 'PRESS')
    kmi = km.keymap_items.new('power_sequencer.border_select', 'B', 'PRESS', shift=True)

    kmi = km.keymap_items.new('power_sequencer.change_playback_speed', 'ONE', 'PRESS', )
    kmi_props_setattr(kmi.properties, "function", "Speed to 1x")
    kmi_props_setattr(kmi.properties, "speed", "normal")

    kmi = km.keymap_items.new('power_sequencer.change_playback_speed', 'TWO', 'PRESS')
    kmi_props_setattr(kmi.properties, "function", "Speed to 1.33x")
    kmi_props_setattr(kmi.properties, "speed", "fast")

    kmi = km.keymap_items.new('power_sequencer.change_playback_speed', 'THREE', 'PRESS')
    kmi_props_setattr(kmi.properties, "function", "Speed to 1.66x")
    kmi_props_setattr(kmi.properties, "speed", "faster")

    kmi = km.keymap_items.new('power_sequencer.change_playback_speed', 'FOUR', 'PRESS')
    kmi_props_setattr(kmi.properties, "function", "Speed to 2x")
    kmi_props_setattr(kmi.properties, "speed", "double")

    kmi = km.keymap_items.new('power_sequencer.channel_offset', 'UP_ARROW', 'PRESS', alt=True)
    kmi_props_setattr(kmi.properties, 'function', 'Move to Open Channel Above')
    kmi_props_setattr(kmi.properties, 'direction', 'up')

    kmi = km.keymap_items.new('power_sequencer.channel_offset', 'DOWN_ARROW', 'PRESS', alt=True)
    kmi_props_setattr(kmi.properties, 'function', 'Move to Open Channel Below')
    kmi_props_setattr(kmi.properties, 'direction', 'down')

    kmi = km.keymap_items.new('power_sequencer.clear_fades', 'F', 'PRESS', alt=True, ctrl=True)

    kmi = km.keymap_items.new('power_sequencer.concatenate_strips', 'C', 'PRESS')
    kmi_props_setattr(kmi.properties, 'function', 'Concatenate selected strips in channel, or concatenate & select next strip in channel if only 1 strip selected')
    kmi_props_setattr(kmi.properties, 'concatenate_whole_channel', False)

    kmi = km.keymap_items.new('power_sequencer.concatenate_strips', 'C', 'PRESS', shift=True)
    kmi_props_setattr(kmi.properties, 'function', 'Concatenate selected strips in channel, or concatenate & select next strip in channel if only 1 strip selected')
    kmi_props_setattr(kmi.properties, 'concatenate_whole_channel', True)

    kmi = km.keymap_items.new('power_sequencer.copy_selected_sequences', 'C', 'PRESS', ctrl=True)
    kmi_props_setattr(kmi.properties, 'function', 'Copy')
    kmi_props_setattr(kmi.properties, 'delete_selection', False)

    kmi = km.keymap_items.new('power_sequencer.copy_selected_sequences', 'X', 'PRESS', ctrl=True)
    kmi_props_setattr(kmi.properties, 'function', 'Cut')
    kmi_props_setattr(kmi.properties, 'delete_selection', True)

    kmi = km.keymap_items.new('power_sequencer.cycle_scenes', 'TAB', 'PRESS', shift=True)
    kmi = km.keymap_items.new('power_sequencer.decrease_playback_speed', 'LEFT_BRACKET', 'PRESS')
    kmi = km.keymap_items.new('power_sequencer.delete_direct', 'DEL', 'PRESS')
    kmi = km.keymap_items.new('power_sequencer.edit_crossfade', 'C', 'PRESS', alt=True)

    kmi = km.keymap_items.new('power_sequencer.fade_strips', 'F', 'PRESS', alt=True)
    kmi_props_setattr(kmi.properties, 'function', 'Fade Right',)
    kmi_props_setattr(kmi.properties, 'fade_type', 'right')

    kmi = km.keymap_items.new('power_sequencer.fade_strips', 'F', 'PRESS', ctrl=True)
    kmi_props_setattr(kmi.properties, 'function', 'Fade Left',)
    kmi_props_setattr(kmi.properties, 'fade_type', 'left')

    kmi = km.keymap_items.new('power_sequencer.fade_strips', 'F', 'PRESS')
    kmi_props_setattr(kmi.properties, 'function', 'Fade Both',)
    kmi_props_setattr(kmi.properties, 'fade_type', 'both')

    kmi = km.keymap_items.new('power_sequencer.grab_closest_handle_or_cut', 'G', 'PRESS', shift=True, alt=True)
    kmi = km.keymap_items.new('power_sequencer.grab_sequence_handle', 'G', 'PRESS', shift=True)

    kmi = km.keymap_items.new('power_sequencer.import_local_footage', 'I', 'PRESS', shift=True, ctrl=True)
    kmi_props_setattr(kmi.properties, 'keep_audio', True)

    kmi = km.keymap_items.new('power_sequencer.increase_playback_speed', 'RIGHT_BRACKET', 'PRESS')

    kmi = km.keymap_items.new('power_sequencer.mouse_cut', 'ACTIONMOUSE', 'PRESS', ctrl=True, shift=True)
    kmi_props_setattr(kmi.properties, 'function', 'Cut')

    kmi = km.keymap_items.new('power_sequencer.mouse_cut', 'ACTIONMOUSE', 'PRESS', ctrl=True)
    kmi_props_setattr(kmi.properties, 'function', 'Cut on Mousemove, Keep Gap')

    kmi = km.keymap_items.new('power_sequencer.mouse_toggle_mute', 'ACTIONMOUSE', 'PRESS', alt=True)

    kmi = km.keymap_items.new('power_sequencer.mouse_trim', 'SELECTMOUSE', 'PRESS', ctrl=True, alt=True)
    kmi_props_setattr(kmi.properties, 'function', 'Trim Strip, Keep Gap')
    kmi_props_setattr(kmi.properties, 'select_mode', 'smart')

    kmi = km.keymap_items.new('power_sequencer.mouse_trim', 'SELECTMOUSE', 'PRESS', ctrl=True, alt=True, shift=True)
    kmi_props_setattr(kmi.properties, 'function', 'Trim Strip, Remove Gap')
    kmi_props_setattr(kmi.properties, 'select_mode', 'cursor')

    kmi = km.keymap_items.new('power_sequencer.preview_last_cut', 'P', 'PRESS', shift=True)
    kmi = km.keymap_items.new('power_sequencer.preview_to_selection', 'P', 'PRESS', ctrl=True, alt=True)

    kmi = km.keymap_items.new('power_sequencer.render_for_web', 'F12', 'PRESS', alt=True)
    kmi_props_setattr(kmi.properties, 'preset', 'youtube')
    kmi_props_setattr(kmi.properties, 'name_pattern', 'scene')
    kmi_props_setattr(kmi.properties, 'auto_render', True)

    kmi = km.keymap_items.new('power_sequencer.ripple_delete', 'X', 'PRESS', shift=True)
    kmi = km.keymap_items.new('power_sequencer.save_direct', 'S', 'PRESS', ctrl=True)

    kmi = km.keymap_items.new('power_sequencer.smart_snap', 'K', 'PRESS', alt=True)
    kmi_props_setattr(kmi.properties, 'function', 'Trim Strip Right')
    kmi_props_setattr(kmi.properties, 'side', 'right')

    kmi = km.keymap_items.new('power_sequencer.smart_snap', 'K', 'PRESS', ctrl=True)
    kmi_props_setattr(kmi.properties, 'function', 'Trim Strip Left')
    kmi_props_setattr(kmi.properties, 'side', 'left')

    kmi = km.keymap_items.new('power_sequencer.snap_selection_to_cursor', 'S', 'PRESS', alt=True)

    kmi = km.keymap_items.new('power_sequencer.toggle_selected_mute', 'H', 'PRESS', alt=True)
    kmi_props_setattr(kmi.properties, 'function', 'Mute Unselected')
    kmi_props_setattr(kmi.properties, 'use_unselected', True)

    kmi = km.keymap_items.new('power_sequencer.toggle_selected_mute', 'H', 'PRESS')
    kmi_props_setattr(kmi.properties, 'function', 'Mute Selected')
    kmi_props_setattr(kmi.properties, 'use_unselected', False)

    kmi = km.keymap_items.new('power_sequencer.toggle_waveforms', 'W', 'PRESS', alt=True)
    kmi = km.keymap_items.new('power_sequencer.trim_to_surrounding_cuts', 'ACTIONMOUSE', 'PRESS', shift=True, alt=True)
    kmi = km.keymap_items.new('power_sequencer.delete_direct', 'X', 'PRESS')

    kmi = km.keymap_items.new('sequencer.refresh_all', 'R', 'PRESS', shift=True)

    addon_keymaps.append(km)

    bpy.types.Scene.power_sequencer = bpy.props.PointerProperty(
        type=PowerSequencerProperties)

    handlers_register()

    print("Registered {} with {} modules".format(bl_info["name"], len(
        modules)))


def unregister():
    addon_updater_ops.unregister()

    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)

    try:
        bpy.utils.unregister_module(__name__)
    except:
        traceback.print_exc()

    handlers_unregister()
    print("Unregistered {}".format(bl_info["name"]))
