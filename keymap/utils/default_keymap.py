# Available keys found at:
# https://docs.blender.org/api/2.78/bpy.types.KeyMapItem.html

def default_keymap():
    """
    Defines the default keymap
    """
    
    default_keymap = {
        "Sequencer": {
            "SEQUENCE_EDITOR" : {
                "WINDOW": {
                    "power_sequencer.add_crossfade" : ["C", "PRESS", "CTRL", "ALT"],
                    #"power_sequencer.add_numbered_marker" : ["M", "PRESS", "CTRL", "ALT"],
                    "power_sequencer.add_speed" : ["EQUAL", "PRESS", "SHIFT"],
                    #"power_sequencer.add_title_marker" : ["M", "PRESS", "SHIFT", "CTRL"],
                    "power_sequencer.border_select" : ["B", "PRESS", "SHIFT"],
                    "power_sequencer.border_select" : ["B", "PRESS"],
                    "power_sequencer.concatenate_strips" : ["C", "PRESS", "SHIFT"],
                    "power_sequencer.copy_selected_sequences" : ["C", "PRESS", "CTRL"],
                    "power_sequencer.copy_selected_sequences" : ["X", "PRESS", "CTRL"],
                    "power_sequencer.cycle_scenes" : ["TAB", "PRESS", "SHIFT"],
                    "power_sequencer.delete_direct" : ["DEL", "PRESS"],
                    "power_sequencer.edit_crossfade" : ["C", "PRESS", "ALT"],
                    "power_sequencer.fade_strips" : ["F", "PRESS", "ALT"],
                    "power_sequencer.fade_strips" : ["F", "PRESS", "CTRL"],
                    "power_sequencer.fade_strips" : ["F", "PRESS"],
                    "power_sequencer.grab_closest_handle_or_cut" : ["G", "PRESS", "ALT"],
                    "power_sequencer.grab_sequence_handle" : ["G", "PRESS", "SHIFT"],
                    "power_sequencer.import_local_footage" : ["I", "PRESS", "SHIFT", "CTRL"],
                    "power_sequencer.mouse_cut" : ["ACTIONMOUSE", "PRESS", "CTRL", "SHIFT"],
                    "power_sequencer.mouse_cut" : ["ACTIONMOUSE", "PRESS", "CTRL"],
                    "power_sequencer.mouse_cut" : ["SELECTMOUSE", "PRESS", "CTRL"],
                    "power_sequencer.mouse_toggle_mute" : ["ACTIONMOUSE", "PRESS", "ALT"],
                    "power_sequencer.mouse_trim" : ["SELECTMOUSE", "PRESS", "CTRL"],
                    "power_sequencer.mouse_trim" : ["SELECTMOUSE", "PRESS", "SHIFT", "CTRL"],
                    "power_sequencer.channel_offset" : ["DOWN_ARROW", "PRESS", "ALT"],
                    "power_sequencer.channel_offset" : ["UP_ARROW", "PRESS", "ALT"],
                    "power_sequencer.preview_last_cut" : ["P", "PRESS", "SHIFT"],
                    "power_sequencer.render_for_web" : ["F12", "PRESS", "ALT"],
                    "power_sequencer.ripple_delete" : ["X", "PRESS", "SHIFT"],
                    "power_sequencer.save_direct" : ["S", "PRESS", "CTRL"],
                    "power_sequencer.smart_snap" : ["K", "PRESS", "ALT"],
                    "power_sequencer.smart_snap" : ["K", "PRESS", "CTRL"],
                    "power_sequencer.snap_selection_to_cursor" : ["S", "PRESS", "ALT"],
                    "power_sequencer.toggle_preview_selected_strips" : ["P", "PRESS", "CTRL", "ALT"],
                    "power_sequencer.toggle_selected_mute" : ["H", "PRESS", "ALT"],
                    "power_sequencer.toggle_selected_mute" : ["H", "PRESS"],
                    "power_sequencer.toggle_waveforms" : ["W", "PRESS", "ALT"],
                    "power_sequencer.trim_to_surrounding_cuts" : ["ACTIONMOUSE", "PRESS", "SHIFT", "ALT"],
                    "power_sequencer.increase_playback_speed" : ["RIGHT_BRACKET", "PRESS"],
                    "power_sequencer.decrease_playback_speed" : ["LEFT_BRACKET", "PRESS"],
                }
            }
        }
    }
    return default_keymap
