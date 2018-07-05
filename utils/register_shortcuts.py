import bpy


def set_keymap_property(properties, property_name, value):
    try:
        setattr(properties, property_name, value)
    except AttributeError:
        print("Warning: property '%s' not found in keymap item '%s'" %
              (property_name, properties.__class__.__name__))
    except Exception as e:
        print("Warning: %r" % e)


def register_shortcuts():
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
    set_keymap_property(kmi.properties, "function", "Speed to 1x")
    set_keymap_property(kmi.properties, "speed", "normal")

    kmi = km.keymap_items.new('power_sequencer.change_playback_speed', 'TWO', 'PRESS')
    set_keymap_property(kmi.properties, "function", "Speed to 1.33x")
    set_keymap_property(kmi.properties, "speed", "fast")

    kmi = km.keymap_items.new('power_sequencer.change_playback_speed', 'THREE', 'PRESS')
    set_keymap_property(kmi.properties, "function", "Speed to 1.66x")
    set_keymap_property(kmi.properties, "speed", "faster")

    kmi = km.keymap_items.new('power_sequencer.change_playback_speed', 'FOUR', 'PRESS')
    set_keymap_property(kmi.properties, "function", "Speed to 2x")
    set_keymap_property(kmi.properties, "speed", "double")

    kmi = km.keymap_items.new('power_sequencer.channel_offset', 'UP_ARROW', 'PRESS', alt=True)
    set_keymap_property(kmi.properties, 'function', 'Move to Open Channel Above')
    set_keymap_property(kmi.properties, 'direction', 'up')

    kmi = km.keymap_items.new('power_sequencer.channel_offset', 'DOWN_ARROW', 'PRESS', alt=True)
    set_keymap_property(kmi.properties, 'function', 'Move to Open Channel Below')
    set_keymap_property(kmi.properties, 'direction', 'down')

    kmi = km.keymap_items.new('power_sequencer.clear_fades', 'F', 'PRESS', alt=True, ctrl=True)

    kmi = km.keymap_items.new('power_sequencer.concatenate_strips', 'C', 'PRESS')
    set_keymap_property(kmi.properties, 'function', 'Concatenate selected strips in channel, or concatenate & select next strip in channel if only 1 strip selected')
    set_keymap_property(kmi.properties, 'concatenate_whole_channel', False)

    kmi = km.keymap_items.new('power_sequencer.concatenate_strips', 'C', 'PRESS', shift=True)
    set_keymap_property(kmi.properties, 'function', 'Concatenate selected strips in channel, or concatenate & select next strip in channel if only 1 strip selected')
    set_keymap_property(kmi.properties, 'concatenate_whole_channel', True)

    kmi = km.keymap_items.new('power_sequencer.copy_selected_sequences', 'C', 'PRESS', ctrl=True)
    set_keymap_property(kmi.properties, 'function', 'Copy')
    set_keymap_property(kmi.properties, 'delete_selection', False)

    kmi = km.keymap_items.new('power_sequencer.copy_selected_sequences', 'X', 'PRESS', ctrl=True)
    set_keymap_property(kmi.properties, 'function', 'Cut')
    set_keymap_property(kmi.properties, 'delete_selection', True)

    kmi = km.keymap_items.new('power_sequencer.cycle_scenes', 'TAB', 'PRESS', shift=True)
    kmi = km.keymap_items.new('power_sequencer.decrease_playback_speed', 'LEFT_BRACKET', 'PRESS')
    kmi = km.keymap_items.new('power_sequencer.delete_direct', 'DEL', 'PRESS')
    kmi = km.keymap_items.new('power_sequencer.edit_crossfade', 'C', 'PRESS', alt=True)

    kmi = km.keymap_items.new('power_sequencer.fade_strips', 'F', 'PRESS', alt=True)
    set_keymap_property(kmi.properties, 'function', 'Fade Right',)
    set_keymap_property(kmi.properties, 'fade_type', 'right')

    kmi = km.keymap_items.new('power_sequencer.fade_strips', 'F', 'PRESS', ctrl=True)
    set_keymap_property(kmi.properties, 'function', 'Fade Left',)
    set_keymap_property(kmi.properties, 'fade_type', 'left')

    kmi = km.keymap_items.new('power_sequencer.fade_strips', 'F', 'PRESS')
    set_keymap_property(kmi.properties, 'function', 'Fade Both',)
    set_keymap_property(kmi.properties, 'fade_type', 'both')

    kmi = km.keymap_items.new('power_sequencer.grab_closest_handle_or_cut', 'G', 'PRESS', shift=True, alt=True)
    kmi = km.keymap_items.new('power_sequencer.grab_sequence_handle', 'G', 'PRESS', shift=True)

    kmi = km.keymap_items.new('power_sequencer.import_local_footage', 'I', 'PRESS', shift=True, ctrl=True)
    set_keymap_property(kmi.properties, 'keep_audio', True)

    kmi = km.keymap_items.new('power_sequencer.increase_playback_speed', 'RIGHT_BRACKET', 'PRESS')

    kmi = km.keymap_items.new('power_sequencer.mouse_cut', 'ACTIONMOUSE', 'PRESS', ctrl=True, shift=True)
    set_keymap_property(kmi.properties, 'function', 'Cut')

    kmi = km.keymap_items.new('power_sequencer.mouse_cut', 'ACTIONMOUSE', 'PRESS', ctrl=True)
    set_keymap_property(kmi.properties, 'function', 'Cut on Mousemove, Keep Gap')

    kmi = km.keymap_items.new('power_sequencer.mouse_toggle_mute', 'ACTIONMOUSE', 'PRESS', alt=True)

    kmi = km.keymap_items.new('power_sequencer.mouse_trim', 'SELECTMOUSE', 'PRESS', ctrl=True, alt=True)
    set_keymap_property(kmi.properties, 'function', 'Trim Strip, Keep Gap')
    set_keymap_property(kmi.properties, 'select_mode', 'smart')

    kmi = km.keymap_items.new('power_sequencer.mouse_trim', 'SELECTMOUSE', 'PRESS', ctrl=True, alt=True, shift=True)
    set_keymap_property(kmi.properties, 'function', 'Trim Strip, Remove Gap')
    set_keymap_property(kmi.properties, 'select_mode', 'cursor')

    kmi = km.keymap_items.new('power_sequencer.preview_last_cut', 'P', 'PRESS', shift=True)
    kmi = km.keymap_items.new('power_sequencer.preview_to_selection', 'P', 'PRESS', ctrl=True, alt=True)

    kmi = km.keymap_items.new('power_sequencer.render_for_web', 'F12', 'PRESS', alt=True)
    set_keymap_property(kmi.properties, 'preset', 'youtube')
    set_keymap_property(kmi.properties, 'name_pattern', 'scene')
    set_keymap_property(kmi.properties, 'auto_render', True)

    kmi = km.keymap_items.new('power_sequencer.ripple_delete', 'X', 'PRESS', shift=True)
    kmi = km.keymap_items.new('power_sequencer.save_direct', 'S', 'PRESS', ctrl=True)

    kmi = km.keymap_items.new('power_sequencer.smart_snap', 'K', 'PRESS', alt=True)
    set_keymap_property(kmi.properties, 'function', 'Trim Strip Right')
    set_keymap_property(kmi.properties, 'side', 'right')

    kmi = km.keymap_items.new('power_sequencer.smart_snap', 'K', 'PRESS', ctrl=True)
    set_keymap_property(kmi.properties, 'function', 'Trim Strip Left')
    set_keymap_property(kmi.properties, 'side', 'left')

    kmi = km.keymap_items.new('power_sequencer.snap_selection_to_cursor', 'S', 'PRESS', alt=True)

    kmi = km.keymap_items.new('power_sequencer.toggle_selected_mute', 'H', 'PRESS', alt=True)
    set_keymap_property(kmi.properties, 'function', 'Mute Unselected')
    set_keymap_property(kmi.properties, 'use_unselected', True)

    kmi = km.keymap_items.new('power_sequencer.toggle_selected_mute', 'H', 'PRESS')
    set_keymap_property(kmi.properties, 'function', 'Mute Selected')
    set_keymap_property(kmi.properties, 'use_unselected', False)

    kmi = km.keymap_items.new('power_sequencer.toggle_waveforms', 'W', 'PRESS', alt=True)
    kmi = km.keymap_items.new('power_sequencer.trim_to_surrounding_cuts', 'ACTIONMOUSE', 'PRESS', shift=True, alt=True)
    kmi = km.keymap_items.new('power_sequencer.delete_direct', 'X', 'PRESS')

    kmi = km.keymap_items.new('sequencer.refresh_all', 'R', 'PRESS', shift=True)
    return km
