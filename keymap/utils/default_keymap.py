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
                    "power_sequencer.add_crossfade" : {
                        "0" : ["C", "CTRL", "ALT"]
                    },
                    "power_sequencer.add_speed" : {
                        "0" : ["EQUAL", "SHIFT"]
                    },
                    "power_sequencer.border_select" : {
                        "0" : ["B", "SHIFT"]
                    },
                    "power_sequencer.change_playback_speed" : {
                        "0" : ["ONE"],
                        "1" : ["TWO"],
                        "2" : ["THREE"],
                        "3" : ["FOUR"]
                    },
                    "power_sequencer.channel_offset" : {
                        "0" : ["DOWN_ARROW", "ALT"],
                        "1" : ["UP_ARROW", "ALT"]
                    },
                    "power_sequencer.channel_offset" : {
                        "0" : ["DOWN_ARROW", "ALT"],
                        "1" : ["UP_ARROW", "ALT"]
                    },
                    "power_sequencer.concatenate_strips" : {
                        "0" : ["C", "SHIFT"]
                    },
                    "power_sequencer.copy_selected_sequences" : {
                        "0" : ["C", "PRESS", "CTRL"],
                        "1" : ["X", "PRESS", "CTRL"]
                    },
                    "power_sequencer.cycle_scenes" : {
                        "0" : ["TAB", "SHIFT"]
                    },
                    "power_sequencer.decrease_playback_speed" : {
                        "0" : ["LEFT_BRACKET", "PRESS"]
                    },
                    "power_sequencer.delete_direct" : {
                        "0" : ["DEL", "PRESS"]
                    },
                    "power_sequencer.edit_crossfade" : {
                        "0" : ["C", "ALT"]
                    },
                    "power_sequencer.fade_strips" : {
                        "0" : ["F", "ALT"],
                        "1" : ["F", "CTRL"],
                        "2" : ["F", "PRESS"]
                    },
                    "power_sequencer.grab_closest_handle_or_cut" : {
                        "0" : ["G", "ALT"]
                    },
                    "power_sequencer.grab_sequence_handle" : {
                        "0" : ["G", "SHIFT"]
                    },
                    "power_sequencer.import_local_footage" : {
                        "0" : ["I", "SHIFT", "CTRL"]
                    },
                    "power_sequencer.increase_playback_speed" : {
                        "0" : ["RIGHT_BRACKET", "PRESS"]
                    },
                    "power_sequencer.mouse_cut" : {
                        "0" : ["ACTIONMOUSE", "CTRL", "SHIFT"],
                        "1" : ["ACTIONMOUSE", "CTRL"],
                        "2" : ["SELECTMOUSE", "CTRL"]
                    },
                    "power_sequencer.mouse_toggle_mute" : {
                        "0" : ["ACTIONMOUSE", "ALT"]
                    },
                    "power_sequencer.mouse_trim" : {
                        "0" : ["SELECTMOUSE", "CTRL"],
                        "1" : ["SELECTMOUSE", "SHIFT", "CTRL"]
                    },
                    "power_sequencer.preview_last_cut" : {
                        "0" : ["P", "SHIFT"]
                    },
                    "power_sequencer.render_for_web" : {
                        "0" : ["F12", "ALT"]
                    },
                    "power_sequencer.ripple_delete" : {
                        "0" : ["X", "SHIFT"]
                    },
                    "power_sequencer.save_direct" : {
                        "0" : ["S", "CTRL"]
                    },
                    "power_sequencer.smart_snap" : {
                        "0" : ["K", "ALT"],
                        "1" : ["K", "CTRL"]
                    },
                    "power_sequencer.snap_selection_to_cursor" : {
                        "0" : ["S", "ALT"]
                    },
                    "power_sequencer.toggle_preview_selected_strips" : {
                        "0" : ["P", "CTRL", "ALT"]
                    },
                    "power_sequencer.toggle_selected_mute" : {
                        "0" : ["H", "ALT"],
                        "1" : ["H", "PRESS"]
                    },
                    "power_sequencer.toggle_waveforms" : {
                        "0" : ["W", "ALT"]
                    },
                    "power_sequencer.trim_to_surrounding_cuts" : {
                        "0" : ["ACTIONMOUSE", "SHIFT", "ALT"]
                    }
                }
            }
        }
    }

    return default_keymap