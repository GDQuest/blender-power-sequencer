# Available keys found at:
# https://docs.blender.org/api/blender_python_api_2_78_release/bpy.types.KeyMapItem.html?highlight=keymap_item

def default():
    """
    Defines the default keymap

    multiple kmi properties are separated with a ';'

        "properties=attribute_1:value_1; attribute_2:value_2"

    values must be string, int, float, or bool

    Check the api to see which attributes can be set here:
    https://docs.blender.org/api/blender_python_api_2_77_0/bpy.types.KeyMapItems.html#bpy.types.KeyMapItems.new

    By default all kmi's "value" attribute will be "PRESS"
    """

    default_keymap = {
        "Sequencer": {
            "SEQUENCE_EDITOR" : {
                "WINDOW": {
                    "power_sequencer.add_crossfade" : {
                        "0" : ["type=C", "ctrl=True", "alt=True"]
                    },
                    "power_sequencer.add_speed" : {
                        "0" : ["type=PLUS", "shift=True"]
                    },
                    "power_sequencer.add_transform" : {
                        "0" : ["type=T"]
                    },
                    "power_sequencer.border_select" : {
                        "0" : ["type=B", "shift=True"]
                    },
                    "power_sequencer.change_playback_speed" : {
                        "0" : ["type=ONE", "properties=function:Speed to 1x; speed:normal"],
                        "1" : ["type=TWO", "properties=function:Speed to 1.33x; speed:fast"],
                        "2" : ["type=THREE", "properties=function:Speed to 1.66x; speed:faster"],
                        "3" : ["type=FOUR", "properties=function: Speed to 2x; speed:double"]
                    },
                    "power_sequencer.channel_offset" : {
                        "0" : ["type=UP_ARROW", "alt=True", "properties=function:Move to Open Channel Above; direction:up"],
                        "1" : ["type=DOWN_ARROW", "alt=True", "properties=function:Move to Open Channel Below; direction:down"]
                    },
                    "power_sequencer.clear_fades": {
                        "0": ["type=F", "alt=True", "ctrl=True"]
                    },
                    "power_sequencer.concatenate_strips" : {
                        "0" : ["type=C", "properties=function:Concatenate selected strips in channel, or concatenate & select next strip in channel if only 1 strip selected; concatenate_whole_channel:False"],
                        "1" : ["type=C", "shift=True", "properties=function:Concatenate selected strips in channel, or concatenate all strips in channel if only 1 strip selected;concatenate_whole_channel:True"]
                    },
                    "power_sequencer.copy_selected_sequences" : {
                        "0" : ["type=C", "ctrl=True", "properties=function:Copy; delete_selection:False"],
                        "1" : ["type=X", "ctrl=True", "properties=function:Cut; delete_selection:True"]
                    },
                    "power_sequencer.cycle_scenes" : {
                        "0" : ["type=TAB", "shift=True"]
                    },
                    "power_sequencer.decrease_playback_speed" : {
                        "0" : ["type=LEFT_BRACKET"]
                    },
                    "power_sequencer.delete_direct" : {
                        "0" : ["type=DEL"]
                    },
                    "power_sequencer.edit_crossfade" : {
                        "0" : ["type=C", "alt=True"]
                    },
                    "power_sequencer.fade_strips" : {
                        "0" : ["type=F", "alt=True", "properties=function:Fade Right; fade_type:right"],
                        "1" : ["type=F", "ctrl=True", "properties=function: Fade Left; fade_type:left"],
                        "2" : ["type=F", "properties=function: Fade Both; fade_type:both"]
                    },
                    "power_sequencer.grab_closest_handle_or_cut" : {
                        "0" : ["type=G", "shift=True", "alt=True"]
                    },
                    "power_sequencer.grab_sequence_handle" : {
                        "0" : ["type=G", "shift=True"]
                    },
                    "power_sequencer.import_local_footage" : {
                        "0" : ["type=I", "shift=True", "ctrl=True", "properties=keep_audio:True"]
                    },
                    "power_sequencer.increase_playback_speed" : {
                        "0" : ["type=RIGHT_BRACKET"]
                    },
                    "power_sequencer.mouse_cut" : {
                        "0" : ["type=ACTIONMOUSE", "ctrl=True", "shift=True", "properties=function:Cut"],
                        "1" : ["type=ACTIONMOUSE", "ctrl=True", "properties=function:Cut on Mousemove, Keep Gap"]
                    },
                    "power_sequencer.mouse_toggle_mute" : {
                        "0" : ["type=ACTIONMOUSE", "alt=True"]
                    },
                    "power_sequencer.mouse_trim" : {
                        "0" : ["type=SELECTMOUSE", "ctrl=True",  "alt=True", "properties=function:Trim Strip, Keep Gap;select_mode:smart"],
                        "1" : ["type=SELECTMOUSE", "shift=True", "ctrl=True", "alt=True", "properties=function:Trim Strip, Remove Gap; select_mode:cursor"]
                    },
                    "power_sequencer.preview_last_cut" : {
                        "0" : ["type=P", "shift=True"]
                    },
                    "power_sequencer.render_for_web" : {
                        "0" : ["type=F12", "alt=True", "properties=preset:youtube; name_pattern:scene; auto_render:True"]
                    },
                    "power_sequencer.ripple_delete" : {
                        "0" : ["type=X", "shift=True"]
                    },
                    "power_sequencer.save_direct" : {
                        "0" : ["type=S", "ctrl=True"]
                    },
                    "power_sequencer.smart_snap" : {
                        "0" : ["type=K", "alt=True", "properties=function:Trim Strip Right; side:right"],
                        "1" : ["type=K", "ctrl=True", "properties=function:Trim Strip Left; side:left"]
                    },
                    "power_sequencer.snap_selection_to_cursor" : {
                        "0" : ["type=S", "alt=True"]
                    },
                    "power_sequencer.preview_to_selection" : {
                        "0" : ["type=P", "ctrl=True", "alt=True"]
                    },
                    "power_sequencer.toggle_selected_mute" : {
                        "0" : ["type=H", "alt=True", "properties=function:Mute Unselected; use_unselected:True"],
                        "1" : ["type=H", "properties=function:Mute Selected; use_unselected:False"]
                    },
                    "power_sequencer.toggle_waveforms" : {
                        "0" : ["type=W", "alt=True"]
                    },
                    "power_sequencer.trim_to_surrounding_cuts" : {
                        "0" : ["type=ACTIONMOUSE", "shift=True", "alt=True"]
                    },
                    "power_sequencer.delete_direct" : {
                        "0" : ["type=X"]
                    },
                    "sequencer.refresh_all" : {
                        "0" : ["type=R", "shift=True"]
                    },
                }
            }
        }
    }

    return default_keymap
