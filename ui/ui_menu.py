import bpy

class PowerSequencerUIMenu(bpy.types.Menu):
    bl_idname = "SEQUENCER_MT_power_sequencer"
    bl_label = "Power Sequencer"

    def draw(self, context):
        layout = self.layout
        
        layout.operator(
            "power_sequencer.synchronize_titles"
        )
        layout.operator(
            "power_sequencer.set_timeline_range"
        )
        layout.operator(
            "power_sequencer.cycle_scenes"
        )
        layout.operator(
            "power_sequencer.channel_offset"
        )
        layout.separator()
        layout.menu(
            "PS_MT_trim"
        )
        layout.menu(
            "PS_MT_strips"
        )
        layout.menu(
            "PS_MT_select"
        )
        layout.menu(
            "PS_MT_render"
        )
        layout.menu(
            "PS_MT_playback"
        )
        layout.menu(
            "PS_MT_markers"
        )
        layout.menu(
            "PS_MT_file"
        )
        layout.menu(
            "PS_MT_edit"
        )
        layout.menu(
            "PS_MT_audio"
        )

class PS_MT_playback(bpy.types.Menu):
    bl_label = "Playback Speed"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "power_sequencer.increase_playback_speed"
        )
        layout.operator(
            "power_sequencer.decrease_playback_speed"
        )
        layout.operator(
            "power_sequencer.change_playback_speed"
        )

class PS_MT_strips(bpy.types.Menu):
    bl_label = "Strips Operation"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "power_sequencer.add_transform"
        )
        layout.separator()
        layout.menu(
            "PS_MT_strips_speed"
        )
        layout.operator(
            "power_sequencer.concatenate_strips"
        )
        layout.operator(
            "power_sequencer.fade_strips"
        )
        layout.operator(
            "power_sequencer.swap_strips"
        )
        layout.operator(
            "power_sequencer.toggle_selected_mute"
        )
        layout.separator()
        layout.menu(
            "PS_MT_strips_fades"
        )

class PS_MT_strips_speed (bpy.types.Menu):
    bl_label = "Speed"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "power_sequencer.add_speed"
        )
        layout.operator(
            "power_sequencer.unspeed"
        )

class PS_MT_strips_fades (bpy.types.Menu):
    bl_label = "Fade in/out"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "power_sequencer.fade_add"
        )
        layout.operator(
            "power_sequencer.fade_clear"
        )

class PS_MT_select(bpy.types.Menu):
    bl_label = "Select"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "power_sequencer.border_select"
        )
        layout.operator(
            "power_sequencer.select_linked_effect"
        )
        layout.menu(
            "PS_MT_deselect"
        )
        layout.separator()
        layout.menu(
            "PS_MT_grab"
        )
        layout.menu(
            "PS_MT_snap"
        )

class PS_MT_deselect(bpy.types.Menu):
    bl_label = "Deselect"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "power_sequencer.deselect_all_left_or_right"
        )
        layout.operator(
            "power_sequencer.deselect_handles_and_grab"
        )

class PS_MT_grab(bpy.types.Menu):
    bl_label = "Grab"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "power_sequencer.grab"
        )
        layout.operator(
            "power_sequencer.grab_closest_cut"
        )
        layout.operator(
            "power_sequencer.grab_sequence_handle"
        )

class PS_MT_snap(bpy.types.Menu):
    bl_label = "Snap"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "power_sequencer.smart_snap"
        )
        layout.operator(
            "power_sequencer.snap_selection_to_cursor"
        )

class PS_MT_edit(bpy.types.Menu):
    bl_label = "Edit"

    def draw(self, context):
        layout = self.layout

        layout.menu(
            "PS_MT_delete"
        )
        layout.separator()
        layout.operator(
            "power_sequencer.remove_gaps"
        )
        layout.operator(
            "power_sequencer.copy_selected_sequences"
        )

class PS_MT_delete(bpy.types.Menu):
    bl_label = "Delete"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "power_sequencer.delete_direct"
        )
        layout.operator(
            "power_sequencer.ripple_delete"
        )

class PS_MT_markers(bpy.types.Menu):
    bl_label = "Markers"

    def draw(self, context):
        layout = self.layout

        layout.menu(
            "PS_MT_marker_delete"
        )
        layout.separator()
        layout.operator(
            "power_sequencer.go_to_next_marker"
        )
        layout.operator(
            "power_sequencer.markers_as_timecode"
        )
        layout.operator(
            "power_sequencer.snap_marker_to_cursor"
        )
        layout.operator(
            "power_sequencer.set_preview_between_markers"
        )
        layout.operator(
            "power_sequencer.markers_snap_matching_strips"
        )

class PS_MT_marker_delete(bpy.types.Menu):
    bl_label = "Delete Marker"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "power_sequencer.marker_delete_closest"
        )
        layout.operator(
            "power_sequencer.markers_delete_direct"
        )

class PS_MT_render(bpy.types.Menu):
    bl_label = "Render"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "power_sequencer.make_still_image"
        )
        layout.operator(
            "power_sequencer.render_for_web"
        )


class PS_MT_file(bpy.types.Menu):
    bl_label = "File"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "power_sequencer.open_project_directory"
        )
        layout.operator(
            "power_sequencer.save_direct"
        )
        layout.operator(
            "power_sequencer.import_local_footage"
        )
        layout.operator(
            "power_sequencer.set_video_proxies"
        )

class PS_MT_trim(bpy.types.Menu):
    bl_label = "Trim"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "power_sequencer.trim_three_point_edit"
        )
        layout.operator(
            "power_sequencer.trim_to_surrounding_cuts"
        )
        layout.separator()
        layout.menu(
            "PS_MT_mouse"
        )
        layout.separator()
        layout.menu(
            "PS_MT_preview"
        )

class PS_MT_mouse(bpy.types.Menu):
    bl_label = "Mouse Trim"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "power_sequencer.mouse_cut"
        )
        layout.operator(
            "power_sequencer.mouse_trim"
        )

class PS_MT_preview(bpy.types.Menu):
    bl_label = "Preview"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "power_sequencer.preview_last_cut"
        )
        layout.operator(
            "power_sequencer.preview_to_selection"
        )

class PS_MT_audio(bpy.types.Menu):
    bl_label = "Audio"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "power_sequencer.align_audios"
        )
        layout.operator(
            "power_sequencer.toggle_waveforms"
        )
        layout.operator(
            "power_sequencer.mouse_toggle_mute"
        )
        layout.separator()
        layout.menu(
            "PS_MT_crossfade"
        )

class PS_MT_crossfade(bpy.types.Menu):
    bl_label = "Crossfade"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "power_sequencer.crossfade_add"
        )
        layout.operator(
            "power_sequencer.crossfade_edit"
        )
        layout.operator(
            "power_sequencer.crossfade_remove"
        )
