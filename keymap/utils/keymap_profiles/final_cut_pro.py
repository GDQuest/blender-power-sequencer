# this profile developed using Paul O Caggegi's guide:
# http://www.paulcaggegi.com/video-editing-using-the-blender-vse/

def final_cut_pro():
    final_cut_pro_keymap = {
        "Frames" : {
            "EMPTY" : {
                "WINDOW" : {
                    "screen.animation_cancel" : {
                        "0" : ["type=ESC"],
                        "1" : ["type=MEDIA_STOP"],
                        "2" : ["type=K", "properties=restore_frame:False"]
                    },
                    "screen.animation_play" : {
                        "0" : ["type=L"],
                        "1" : ["type=J", "properties=reverse:True"],
                        "2" : ["type=MEDIA_PLAY"],
                        "3" : ["type=SPACE"]
                    },
                    "screen.frame_jump" : {
                        "0" : ["type=UP_ARROW", "shift=True", "ctrl=True", "properties=end:True"],
                        "1" : ["type=DOWN_ARROW", "shift=True", "ctrl=True", "properties=end:False"],
                        "2" : ["type=RIGHT_ARROW", "shift=True", "properties=end:True"],
                        "3" : ["type=LEFT_ARROW", "shift=True", "properties=end:False"]
                    },
                    "screen.frame_offset" : {
                        "0" : ["type=UP_ARROW", "shift=True", "properties=delta:10"],
                        "1" : ["type=DOWN_ARROW", "shift=True", "properties=delta:-10"],
                        "2" : ["type=LEFT_ARROW", "properties=delta:-1"],
                        "3" : ["type=RIGHT_ARROW", "properties=delta:1"],
                        "4" : ["type=WHEELDOWNMOUSE", "alt=True", "properties=delta:1"],
                        "5" : ["type=WHEELUPMOUSE", "alt=True", "properties=delta:-1"]
                    },
                    "screen.keyframe_jump" : {
                        "0" : ["type=UP_ARROW", "alt=True", "properties=next:True"],
                        "1" : ["type=DOWN_ARROW", "alt=True", "properties=next:False"],
                        "2" : ["type=MEDIA_LAST", "properties=next:True"],
                        "3" : ["type=MEDIA_FIRST", "properties=next:False"]
                    }
                }
            }
        },
        "Sequencer" : {
            "SEQUENCE_EDITOR" : {
                "WINDOW" : {
                    "marker.add" : {
                        "0" : ["type=M"]
                    },
                    "marker.rename" : {
                        "0" : ["type=M", "ctrl=True"]
                    },
                    "sequencer.copy" : {
                        "0" : ["type=C", "ctrl=True"],
                        "1" : ["type=C", "oskey=True"]
                    },
                    "sequencer.cut" : {
                        "0" : ["type=B", "properties=type:SOFT"],
                        "1" : ["type=B", "shift=True", "properties=type:HARD"]
                    },
                    "sequencer.cut_multicam" : {
                        "0" : ["type=ONE", "properties=camera:1"],
                        "1" : ["type=TWO", "properties=camera:2"],
                        "2" : ["type=THREE", "properties=camera:3"],
                        "3" : ["type=FOUR", "properties=camera:4"],
                        "4" : ["type=FIVE", "properties=camera:5"],
                        "5" : ["type=SIX", "properties=camera:6"],
                        "6" : ["type=SEVEN", "properties=camera:7"],
                        "7" : ["type=EIGHT", "properties=camera:8"],
                        "8" : ["type=NINE", "properties=camera:9"],
                        "9" : ["type=ZERO", "properties=camera:10"]
                    },
                    "sequencer.delete" : {
                        "0" : ["type=X"],
                        "1" : ["type=DEL"]
                    },
                    "sequencer.duplicate_move" : {
                        "0" : ["type=D", "shift=True"]
                    },
                    "sequencer.gap_insert" : {
                        "0" : ["type=EQUAL", "shift=True"]
                    },
                    "sequencer.gap_remove" : {
                        "0" : ["type=BACK_SPACE", "properties=all:False"],
                        "1" : ["type=BACK_SPACE", "shift=True", "properties=all:True"]
                    },
                    "sequencer.images_separate" : {
                        "0" : ["type=Y"]
                    },
                    "sequencer.lock" : {
                        "0" : ["type=L", "shift=True"]
                    },
                    "sequencer.meta_make" : {
                        "0" : ["type=G", "ctrl=True"]
                    },
                    "sequencer.meta_separate" : {
                        "0" : ["type=G", "alt=True"]
                    },
                    "sequencer.meta_toggle" : {
                        "0" : ["type=TAB"]
                    },
                    "sequencer.mute" : {
                        "0" : ["type=H", "properties=unselected:False"],
                        "1" : ["type=H", "shift=True", "properties=unselected:True"]
                    },
                    "sequencer.offset_clear" : {
                        "0" : ["type=O", "alt=True"]
                    },
                    "sequencer.paste" : {
                        "0" : ["type=V", "ctrl=True"],
                        "1" : ["type=V", "oskey=True"]
                    },
                    "sequencer.reassign_inputs" : {
                        "0" : ["type=R"]
                    },
                    "sequencer.reload" : {
                        "0" : ["type=R", "alt=True"],
                        "1" : ["type=R", "alt=True", "shift=True", "properties=adjust_length:True"]
                    },
                    "sequencer.select" : {
                        "0" : ["type=SELECTMOUSE", "properties=extend:False; linked_handle:False; left_right:NONE; linked_time:False"],
                        "1" : ["type=SELECTMOUSE", "shift=True", "properties=extend:True; linked_handle:False; left_right:NONE; linked_time:False"],
                        "2" : ["type=SELECTMOUSE", "alt=True", "properties=extend:False; linked_handle:True; left_right:NONE; linked_time:False"],
                        "3" : ["type=SELECTMOUSE", "alt=True", "shift=True", "properties=extend:True; linked_handle:True; left_right:NONE; linked_time:False"],
                        "4" : ["type=SELECTMOUSE", "ctrl=True", "properties=extend:False; linked_handle:False; left_right:MOUSE; linked_time:True"],
                        "5" : ["type=SELECTMOUSE", "shift=True", "ctrl=True", "properties=extend:True; linked_handle:False; left_right:NONE; linked_time:True"]
                    },
                    "sequencer.select_all" : {
                        "0" : ["type=A", "properties=action:TOGGLE"],
                        "1" : ["type=I", "ctrl=True", "properties=action:INVERT"]
                    },
                    "sequencer.select_border" : {
                        "0" : ["type=EVT_TWEAK_L", "value=ANY", "properties=extend:True"]
                    },
                    "sequencer.select_grouped" : {
                        "0" : ["type=G", "shift=True"]
                    },
                    "sequencer.select_less" : {
                        "0" : ["type=NUMPAD_MINUS", "ctrl=True"]
                    },
                    "sequencer.select_linked" : {
                        "0" : ["type=L", "ctrl=True"]
                    },
                    "sequencer.select_linked_pick" : {
                        "0" : ["type=L", "properties=extend:False"],
                        "1" : ["type=L", "shift=True", "properties=extend:True"]
                    },
                    "sequencer.select_more" : {
                        "0" : ["type=NUMPAD_PLUS", "ctrl=True"]
                    },
                    "sequencer.slip" : {
                        "0" : ["type=S"]
                    },
                    "sequencer.snap" : {
                        "0" : ["type=S", "shift=True"]
                    },
                    "sequencer.strip_jump" : {
                        "0" : ["type=PAGE_UP", "properties=next:True; center:False"],
                        "1" : ["type=PAGE_DOWN", "properties=next:False; center:False"],
                        "2" : ["type=UP_ARROW", "properties=next:True; center:False"],
                        "3" : ["type=DOWN_ARROW", "properties=next:False; center:False"]
                    },
                    "sequencer.swap" : {
                        "0" : ["type=LEFT_ARROW", "alt=True", "properties=side:LEFT"],
                        "1" : ["type=RIGHT_ARROW", "alt=True", "properties=side:RIGHT"]
                    },
                    "sequencer.swap_inputs" : {
                        "0" : ["type=S", "alt=True"]
                    },
                    "sequencer.unlock" : {
                        "0" : ["type=L", "alt=True", "shift=True"]
                    },
                    "sequencer.unmute" : {
                        "0" : ["type=H", "alt=True", "properties=unselected:False"],
                        "1" : ["type=H", "alt=True", "shift=True", "properties=unselected:True"]
                    },
                    "sequencer.view_all" : {
                        "0" : ["type=Z", "shift=True"],
                        "1" : ["type=NDOF_BUTTON_FIT"]
                    },
                    "sequencer.view_frame" : {
                        "0" : ["type=NUMPAD_0"]
                    },
                    "sequencer.view_selected" : {
                        "0" : ["type=NUMPAD_0", "shift=True"]
                    },
                    "transform.seq_slide" : {
                        "0" : ["type=G"],
                        "1" : ["type=EVT_TWEAK_S", "value=ANY"]
                    },
                    "transform.transform" : {
                        "0" : ["type=E", "properties=mode:TIME_EXTEND"]
                    },
                    "wm.call_menu" : {
                        "0" : ["type=K", "alt=True", "properties=name:vseqf.quickcuts_menu"],
                        "1" : ["type=P", "ctrl=True", "properties=name:vseqf.quickparents_menu"],
                        "2" : ["type=M", "alt=True", "properties=name:vseqf.quickmarkers_menu"],
                        "3" : ["type=K", "alt=True", "properties=name:vseqf.quickcuts_menu"],
                        "4" : ["type=M", "alt=True", "properties=name:vseqf.quickmarkers_menu"],
                        "5" : ["type=K", "alt=True", "properties=name:vseqf.quickcuts_menu"],
                        "6" : ["type=M", "alt=True", "properties=name:vseqf.quickmarkers_menu"],
                        "7" : ["type=A", "shift=True", "properties=name:SEQUENCER_MT_add"],
                        "8" : ["type=C", "properties=name:SEQUENCER_MT_change"]
                    },
                    "wm.context_set_int" : {
                        "0" : ["type=O", "properties=data_path:scene.sequence_editor.overlay_frame; value:0"]
                    }
                }
            }
        },
        "SequencerPreview" : {
            "SEQUENCE_EDITOR" : {
                "WINDOW" : {
                    "sequencer.sample" : {
                        "0" : ["type=ACTIONMOUSE"]
                    },
                    "sequencer.view_all_preview" : {
                        "0" : ["type=Z", "shift=True"],
                        "1" : ["type=NDOF_BUTTON_FIT"]
                    },
                    "sequencer.view_ghost_border" : {
                        "0" : ["type=O"]
                    },
                    "sequencer.view_zoom_ratio" : {
                        "0" : ["type=NUMPAD_1", "properties=ratio:1.0"]
                    }
                }
            }
        }
    }
    
    return final_cut_pro_keymap
