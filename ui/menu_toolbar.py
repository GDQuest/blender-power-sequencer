import bpy


class PowerSequencerMenuToolbar(bpy.types.Menu):
    bl_idname = "SEQUENCER_MT_power_sequencer"
    bl_label = "Power Sequencer"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.set_scene_settings")
        layout.operator("power_sequencer.synchronize_titles", icon='SORTALPHA')
        layout.operator("power_sequencer.set_timeline_range", icon='ARROW_LEFTRIGHT')
        layout.operator("power_sequencer.scene_cycle", icon='SCENE')

        layout.separator()

        layout.menu("PowerSequencer_MT_render", icon='RENDER_ANIMATION')
        layout.menu("PowerSequencer_MT_playback", icon='PLAY')
        layout.menu("PowerSequencer_MT_trim", icon='LINE_DATA')
        layout.menu("PowerSequencer_MT_strips", icon='NLA')
        layout.menu("PowerSequencer_MT_markers", icon='MARKER')
        layout.menu("PowerSequencer_MT_audio", icon='SOUND')
        layout.menu("PowerSequencer_MT_select", icon='RESTRICT_SELECT_OFF')
        layout.menu("PowerSequencer_MT_edit", icon='MODIFIER')
        layout.menu("PowerSequencer_MT_file", icon='FILE_FOLDER')


class PowerSequencer_MT_playback(bpy.types.Menu):
    bl_label = "Playback Speed"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.increase_playback_speed")
        layout.operator("power_sequencer.decrease_playback_speed")
        layout.operator("power_sequencer.change_playback_speed")


class PowerSequencer_MT_strips(bpy.types.Menu):
    bl_label = "Strips Operation"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.add_transform")

        layout.separator()

        layout.menu("PowerSequencer_MT_strips_speed", icon='TIME')
        layout.operator("power_sequencer.concatenate_strips", icon='CONSTRAINT')
        layout.operator("power_sequencer.fade_strips", icon='IMAGE_RGB_ALPHA')
        layout.operator("power_sequencer.swap_strips", icon='ARROW_LEFTRIGHT')
        layout.operator("power_sequencer.toggle_selected_mute", icon='MUTE_IPO_ON')
        layout.operator("power_sequencer.channel_offset", icon='AUTOMERGE_ON')

        layout.separator()

        layout.menu("PowerSequencer_MT_crossfade", icon='IMAGE_RGB_ALPHA')
        layout.menu("PowerSequencer_MT_strips_fades", icon='IMAGE_RGB_ALPHA')

        layout.separator()

        layout.operator("power_sequencer.make_still_image", icon='FILE_IMAGE')


class PowerSequencer_MT_strips_speed (bpy.types.Menu):
    bl_label = "Speed"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.add_speed")
        layout.operator("power_sequencer.speed_remove_effect")


class PowerSequencer_MT_strips_fades (bpy.types.Menu):
    bl_label = "Fade in/out"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.fade_add")
        layout.operator("power_sequencer.fade_clear")


class PowerSequencer_MT_select(bpy.types.Menu):
    bl_label = "Select"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.border_select", icon='BORDER_RECT')
        layout.operator("power_sequencer.select_linked_effect", icon='CONSTRAINT')
        layout.menu("PowerSequencer_MT_deselect", icon='RESTRICT_SELECT_ON')

        layout.separator()

        layout.menu("PowerSequencer_MT_grab", icon='HAND')
        layout.menu("PowerSequencer_MT_snap", icon='SNAP_ON')
        
        layout.separator()
        
        layout.operator('power_sequencer.select_playing_menu')
        layout.operator('power_sequencer.select_left_right_menu')
        layout.operator('power_sequencer.select_handles_menu')


class PowerSequencer_MT_deselect(bpy.types.Menu):
    bl_label = "Deselect"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.deselect_all_strips_left_or_right")
        layout.operator("power_sequencer.deselect_handles_and_grab")


class PowerSequencer_MT_grab(bpy.types.Menu):
    bl_label = "Grab"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.grab")
        layout.operator("power_sequencer.grab_closest_cut")
        layout.operator("power_sequencer.grab_sequence_handles")


class PowerSequencer_MT_snap(bpy.types.Menu):
    bl_label = "Snap"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.smart_snap")
        layout.operator("power_sequencer.snap_selection_to_cursor")


class PowerSequencer_MT_edit(bpy.types.Menu):
    bl_label = "Edit"

    def draw(self, context):
        layout = self.layout
        layout.menu("PowerSequencer_MT_delete", icon='X')

        layout.separator()

        layout.operator("power_sequencer.remove_gaps", icon='FRAME_PREV')
        layout.operator("power_sequencer.copy_selected_sequences", icon='COPYDOWN')


class PowerSequencer_MT_delete(bpy.types.Menu):
    bl_label = "Delete"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.delete_direct")
        layout.operator("power_sequencer.ripple_delete")


class PowerSequencer_MT_markers(bpy.types.Menu):
    bl_label = "Markers"

    def draw(self, context):
        layout = self.layout
        layout.menu("PowerSequencer_MT_marker_delete", icon='X')

        layout.separator()

        layout.operator("power_sequencer.go_to_next_marker", icon='TRIA_RIGHT_BAR')
        layout.operator("power_sequencer.copy_markers_as_timecodes")
        layout.operator("power_sequencer.snap_marker_to_cursor")
        layout.operator("power_sequencer.set_preview_between_markers")
        layout.operator("power_sequencer.markers_snap_matching_strips", icon='NLA')


class PowerSequencer_MT_marker_delete(bpy.types.Menu):
    bl_label = "Delete Marker"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.marker_delete_closest")
        layout.operator("power_sequencer.markers_delete_direct")


class PowerSequencer_MT_render(bpy.types.Menu):
    bl_label = "Render"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.render_for_web")
        layout.operator("power_sequencer.export_sequence")


class PowerSequencer_MT_file(bpy.types.Menu):
    bl_label = "File"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.open_project_directory", icon='FILE_FOLDER')
        layout.operator("power_sequencer.save_direct", icon='FILE_TICK')
        layout.operator("power_sequencer.import_local_footage", icon='FILE_MOVIE')
        layout.operator("power_sequencer.set_video_proxies", icon='EXTERNAL_DATA')


class PowerSequencer_MT_trim(bpy.types.Menu):
    bl_label = "Trim"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.trim_three_point_edit", icon='TRIA_DOWN')
        layout.operator("power_sequencer.trim_to_surrounding_cuts", icon='SNAP_PEEL_OBJECT')

        layout.separator()
        layout.menu("PowerSequencer_MT_mouse", icon='RESTRICT_SELECT_OFF')
        layout.separator()
        layout.menu("PowerSequencer_MT_preview", icon='SEQ_PREVIEW')


class PowerSequencer_MT_mouse(bpy.types.Menu):
    bl_label = "Mouse Trim"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.mouse_cut")
        layout.operator("power_sequencer.mouse_trim")


class PowerSequencer_MT_preview(bpy.types.Menu):
    bl_label = "Preview"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.preview_last_cut")
        layout.operator("power_sequencer.preview_to_selection")


class PowerSequencer_MT_audio(bpy.types.Menu):
    bl_label = "Audio"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.align_audios", icon='ALIGN')
        layout.operator("power_sequencer.toggle_waveforms", icon='RNDCURVE')
        layout.operator("power_sequencer.mouse_toggle_mute", icon='MUTE_IPO_ON')


class PowerSequencer_MT_crossfade(bpy.types.Menu):
    bl_label = "Crossfade"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.crossfade_add")
        layout.operator("power_sequencer.crossfade_edit")
        layout.operator("power_sequencer.crossfade_remove")
