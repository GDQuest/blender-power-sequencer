import bpy


class POWER_SEQUENCER_MT_main(bpy.types.Menu):
    bl_label = "Power Sequencer"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "power_sequencer.synchronize_titles", text="Synchronize Titles", icon="SORTALPHA"
        )
        layout.operator(
            "power_sequencer.set_timeline_range", text="Set Timeline Range", icon="ARROW_LEFTRIGHT"
        )
        layout.operator("power_sequencer.scene_cycle", text="Scene Cycle", icon="SCENE")

        layout.separator()

        layout.menu("POWER_SEQUENCER_MT_render", text="Render", icon="RENDER_ANIMATION")
        layout.menu("POWER_SEQUENCER_MT_playback", text="Playback", icon="PLAY")
        layout.menu("POWER_SEQUENCER_MT_trim", text="Trim", icon="LINE_DATA")
        layout.menu("POWER_SEQUENCER_MT_strips", text="Strips", icon="NLA")
        layout.menu("POWER_SEQUENCER_MT_markers", text="Markers", icon="MARKER")
        layout.menu("POWER_SEQUENCER_MT_audio", text="Audio", icon="SOUND")
        layout.menu("POWER_SEQUENCER_MT_select", text="Select", icon="RESTRICT_SELECT_OFF")
        layout.menu("POWER_SEQUENCER_MT_edit", text="Edit", icon="MODIFIER")
        layout.menu("POWER_SEQUENCER_MT_file", text="File", icon="FILE_FOLDER")


class POWER_SEQUENCER_MT_playback(bpy.types.Menu):
    bl_label = "Playback Speed"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.playback_speed_increase", text="Increase Speed")
        layout.operator("power_sequencer.playback_speed_decrease", text="Decrease Speed")
        layout.operator("power_sequencer.playback_speed_set", text="Change Speed")


class POWER_SEQUENCER_MT_strips(bpy.types.Menu):
    bl_label = "Strips Operation"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.add_transform", text="Add Transform")

        layout.separator()

        layout.operator(
            "power_sequencer.concatenate_strips", text="Concatenate Strips", icon="CONSTRAINT"
        )
        layout.operator("power_sequencer.swap_strips", text="Swap Strips", icon="ARROW_LEFTRIGHT")
        layout.operator(
            "power_sequencer.toggle_selected_mute", text="Toggle Mute", icon="MUTE_IPO_ON"
        )
        layout.operator(
            "power_sequencer.channel_offset", text="Channel Offset", icon="AUTOMERGE_ON"
        )

        layout.separator()

        layout.menu("POWER_SEQUENCER_MT_crossfade", text="Crossfade", icon="IMAGE_RGB_ALPHA")
        layout.menu("POWER_SEQUENCER_MT_strips_fades", text="Fade Strips", icon="IMAGE_RGB_ALPHA")

        layout.separator()

        layout.operator(
            "power_sequencer.make_still_image", text="Make Still Image", icon="FILE_IMAGE"
        )


class POWER_SEQUENCER_MT_strips_fades(bpy.types.Menu):
    bl_label = "Fade in/out"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.fade_add", text="Add Fade")
        layout.operator("power_sequencer.fade_clear", text="Clear Fade")


class POWER_SEQUENCER_MT_select(bpy.types.Menu):
    bl_label = "Select"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "power_sequencer.select_linked_effect", text="Select Linked Effect", icon="CONSTRAINT"
        )
        layout.menu("POWER_SEQUENCER_MT_deselect", text="Deselect", icon="RESTRICT_SELECT_ON")

        layout.separator()

        layout.menu("POWER_SEQUENCER_MT_grab", text="Grab", icon="HAND")
        layout.menu("POWER_SEQUENCER_MT_snap", text="Snap", icon="SNAP_ON")


class POWER_SEQUENCER_MT_deselect(bpy.types.Menu):
    bl_label = "Deselect"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "power_sequencer.deselect_all_strips_left_or_right", text="Deselect Left/Right"
        )
        layout.operator("power_sequencer.deselect_handles_and_grab", text="Deselect Handles & Grab")


class POWER_SEQUENCER_MT_grab(bpy.types.Menu):
    bl_label = "Grab"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.grab", text="Grab")
        layout.operator("power_sequencer.grab_closest_cut", text="Grab Closest Cut")
        layout.operator("power_sequencer.grab_sequence_handles", text="Grab Sequence Handles")


class POWER_SEQUENCER_MT_snap(bpy.types.Menu):
    bl_label = "Snap"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "power_sequencer.trim_left_or_right_handles", text="Trim Left/Right Handles"
        )
        layout.operator("power_sequencer.snap_selection_to_cursor", text="Snap Selection to Cursor")


class POWER_SEQUENCER_MT_edit(bpy.types.Menu):
    bl_label = "Edit"

    def draw(self, context):
        layout = self.layout
        layout.menu("POWER_SEQUENCER_MT_delete", text="Delete", icon="X")

        layout.separator()

        layout.operator("power_sequencer.remove_gaps", text="Remove Gaps", icon="FRAME_PREV")
        layout.operator(
            "power_sequencer.copy_selected_sequences",
            text="Copy Selected Sequences",
            icon="COPYDOWN",
        )


class POWER_SEQUENCER_MT_delete(bpy.types.Menu):
    bl_label = "Delete"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.delete_direct", text="Direct Delete")
        layout.operator("power_sequencer.ripple_delete", text="Ripple Delete")


class POWER_SEQUENCER_MT_markers(bpy.types.Menu):
    bl_label = "Markers"

    def draw(self, context):
        layout = self.layout
        layout.menu("POWER_SEQUENCER_MT_marker_delete", text="Delete Marker", icon="X")

        layout.separator()

        layout.operator(
            "power_sequencer.marker_go_to_next", text="Go to Next Marker", icon="TRIA_RIGHT_BAR"
        )
        layout.operator(
            "power_sequencer.copy_markers_as_timecodes", text="Copy Marker as Timecodes"
        )
        layout.operator("power_sequencer.marker_snap_to_cursor", text="Snap Marker to Cursor")
        layout.operator(
            "power_sequencer.set_preview_between_markers", text="Set Preview Between Markers"
        )
        layout.operator(
            "power_sequencer.markers_snap_matching_strips", text="Snap Matching Strips", icon="NLA"
        )


class POWER_SEQUENCER_MT_marker_delete(bpy.types.Menu):
    bl_label = "Delete Marker"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.marker_delete_closest", text="Delete Closest Marker")
        layout.operator("power_sequencer.marker_delete_direct", text="Direct Delete Marker")


class POWER_SEQUENCER_MT_render(bpy.types.Menu):
    bl_label = "Render"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.render_apply_preset", text="Render for Web")


class POWER_SEQUENCER_MT_file(bpy.types.Menu):
    bl_label = "File"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "power_sequencer.open_project_directory",
            text="Open Project Directory",
            icon="FILE_FOLDER",
        )
        layout.operator("power_sequencer.save_direct", text="Direct Save", icon="FILE_TICK")
        layout.operator(
            "power_sequencer.import_local_footage", text="Import Local Footage", icon="FILE_MOVIE"
        )
        # XXX: there's no `set_video_proxies` operator
        # layout.operator("power_sequencer.set_video_proxies", icon='EXTERNAL_DATA')


class POWER_SEQUENCER_MT_trim(bpy.types.Menu):
    bl_label = "Trim"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "power_sequencer.trim_three_point_edit", text="Trim Three Point Edit", icon="TRIA_DOWN"
        )
        layout.operator(
            "power_sequencer.trim_to_surrounding_cuts",
            text="Trim to Surrounding Cuts",
            icon="SNAP_PEEL_OBJECT",
        )

        layout.separator()
        layout.menu("POWER_SEQUENCER_MT_mouse", text="Mouse", icon="RESTRICT_SELECT_OFF")
        layout.separator()
        layout.menu("POWER_SEQUENCER_MT_preview", text="Preview", icon="SEQ_PREVIEW")


class POWER_SEQUENCER_MT_mouse(bpy.types.Menu):
    bl_label = "Mouse Trim"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.mouse_trim", text="Mouse Trim")
        layout.operator("power_sequencer.mouse_trim_instantly", text="Mouse Trim Instantly")


class POWER_SEQUENCER_MT_preview(bpy.types.Menu):
    bl_label = "Preview"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.preview_closest_cut", text="Preview Closest Cut")
        layout.operator("power_sequencer.preview_to_selection", text="Preview to Selection")


class POWER_SEQUENCER_MT_audio(bpy.types.Menu):
    bl_label = "Audio"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.align_audios", text="Align Audios", icon="ALIGN_LEFT")
        layout.operator(
            "power_sequencer.toggle_waveforms", text="Toggle Waveforms", icon="RNDCURVE"
        )
        layout.operator("power_sequencer.mouse_toggle_mute", text="Toggle Mute", icon="MUTE_IPO_ON")


class POWER_SEQUENCER_MT_crossfade(bpy.types.Menu):
    bl_label = "Crossfade"

    def draw(self, context):
        layout = self.layout
        layout.operator("power_sequencer.crossfade_add", text="Add Crossfade")
        layout.operator("power_sequencer.crossfade_edit", text="Edit Crossfade")
        layout.operator("power_sequencer.crossfade_remove", text="Remove Crossfade")
