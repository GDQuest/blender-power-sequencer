"""Video editing tools for Blender using the mouse"""
from math import floor

import bpy
from bpy.props import BoolProperty, EnumProperty, IntProperty
# import blf

# TODO: move it to separate file and import both here and in video_edit.py
sequence_types = {'video': ('MOVIE', 'MOVIECLIP', 'META', 'SCENE'),
                  'effect': ('CROSS', 'ADD', 'SUBTRACT', 'ALPHA_OVER',
                             'ALPHA_UNDER', 'GAMMA_CROSS', 'MULTIPLY',
                             'OVER_DROP', 'WIPE', 'GLOW', 'TRANSFORM', 'COLOR',
                             'SPEED', 'ADJUSTMENT', 'GAUSSIAN_BLUR'),
                  'sound': 'SOUND',
                  'image': 'IMAGE',
                  'img': 'IMAGE'}


def find_sequence_trim_side(sequence=None, frame=None):
    """Returns the strip's handle the time cursor is closest to"""
    if not sequence and frame:
        return None

    if frame >= sequence.frame_final_duration / 2:
        return 'right'
    else:
        return 'left'


def mouse_select_sequences(frame=None,
                           channel=None,
                           mode='mouse',
                           select_linked=True):
    """Selects sequences based on the mouse position or using the time cursor"""

    selection = []
    sequences = bpy.context.sequences

    if not sequences:
        return []

    for seq in sequences:
        channel_check = True if seq.channel == channel else False
        if channel_check and seq.frame_final_start <= frame <= seq.frame_final_end:
            selection.append(seq)
            if mode == 'mouse' or mode == 'smart' and channel_check:
                break

    if len(selection) > 0:
        # Select linked time sequences
        if select_linked and mode in ('mouse', 'smart'):
            for seq in sequences:
                if seq.channel != selection[0].channel \
                   and seq.frame_final_start == selection[0].frame_final_start \
                   and seq.frame_final_end == selection[0].frame_final_end:
                    selection.append(seq)
    # In smart mode, if we don't get any selection, we select everything
    elif mode == 'smart':
        selection = sequences
    return selection


# TODO: idea - handler to optionnally ripple edit automatically? And/or auto remove gaps on delete?

# Shortcut: Ctrl Click
# TODO: Option to move the time cursor back before the start of sel if trim
# TODO: allow the user to set the selection mode in the preferences
class MouseCut(bpy.types.Operator):
    """Cuts the strip sitting under the mouse"""
    bl_idname = "gdquest_vse.mouse_cut"
    bl_label = "Cut strip with mouse"
    bl_options = {'REGISTER', 'UNDO'}

    select_mode = EnumProperty(
        items=[('mouse', 'Mouse', 'Only select the strip hovered by the mouse'
                ), ('cursor', 'Time cursor',
                    'Select all of the strips the time cursor overlaps'),
               ('smart', 'Smart',
                'Uses the selection if possible, else uses the other modes')],
        name="Selection mode",
        description=
        "Cut only the strip under the mouse or all strips under the time cursor",
        default='smart')
    cut_mode = EnumProperty(
        items=[('cut', 'Cut', 'Cut the strips'), ('trim', 'Trim',
                                                  'Trim the selection')],
        name='Cut mode',
        description='Cut or trim the selection',
        default='cut')
    remove_gaps = BoolProperty(
        name="Remove gaps",
        description="When trimming the sequences, remove gaps automatically",
        default=False)
    auto_move_cursor = BoolProperty(
        name="Auto move cursor",
        description="When trimming the sequence, auto move the cursor if playback is active",
        default=True)
    cursor_offset = IntProperty(
        name="Cursor trim offset",
        description="On trim, during playback, offset the cursor to better see if the cut works",
        default=12,
        min=0
    )

    @classmethod
    def poll(cls, context):
        return context is not None

    def invoke(self, context, event):
        sequencer = bpy.ops.sequencer
        anim = bpy.ops.anim
        selection = bpy.context.selected_sequences

        frame, channel = context.region.view2d.region_to_view(
            x=event.mouse_region_x,
            y=event.mouse_region_y)
        frame = floor(frame)
        channel = floor(channel)

        anim.change_frame(frame=frame)
        select_mode = self.select_mode

        # Strip selection
        if select_mode == 'cursor':
            sequencer.select_all(action='SELECT')
        elif select_mode == 'smart' and selection:
            use_selection = False

            for seq in selection:
                if seq.frame_final_start <= frame <= seq.frame_final_end:
                    use_selection = True

            if not use_selection:
                sequencer.select_all(action='SELECT')
        else:
            # Smart can behave as mouse mode if the user clicks on a strip
            sequences_to_select = mouse_select_sequences(frame, channel,
                                                         select_mode)
            if not sequences_to_select:
                if select_mode == 'mouse':
                    return {"CANCELLED"}
                elif select_mode == 'smart':
                    sequencer.select_all(action='SELECT')
            else:
                sequencer.select_all(action='DESELECT')
                for seq in sequences_to_select:
                    seq.select = True

        # Cut and trim
        if self.cut_mode == 'cut':
            sequencer.cut(frame=bpy.context.scene.frame_current,
                          type='SOFT',
                          side='BOTH')
        else:
            bpy.ops.gdquest_vse.smart_snap(side='auto')

            if self.remove_gaps:
                anim.change_frame(frame=frame - 1)
                sequencer.gap_remove()

                # Move time cursor back
                if self.auto_move_cursor and bpy.context.screen.is_animation_playing:
                    from operator import attrgetter
                    first_seq = sorted(bpy.context.selected_sequences, key=attrgetter('frame_final_start'))[0]
                    frame = first_seq.frame_final_start - self.cursor_offset \
                        if abs(frame - first_seq.frame_final_start) < first_seq.frame_final_duration / 2 \
                        else frame
                    anim.change_frame(frame=frame)

        sequencer.select_all(action='DESELECT')
        return {"FINISHED"}


# FIXME: Currently using seq_slide to move the sequences but creates bugs
#        Check how builtin modal operators work instead
class EditCrossfade(bpy.types.Operator):
    """Selects handles to edit crossfade and gives a preview of the fade point."""
    bl_idname = "gdquest_vse.edit_crossfade"
    bl_label = "Edit crossfade"
    bl_options = {'REGISTER', 'UNDO'}

    show_preview = BoolProperty(
        name="Preview the crossfade",
        description=
        "Gives a preview of the crossfade sides, but can affect performances",
        default=True)

    def __init__(self):
        self.time_cursor_init_frame = bpy.context.scene.frame_current
        self.last_frame, self.frame = 0, 0
        self.seq_1, self.seq_2 = None, None
        self.crossfade_duration = None
        self.preview_ratio = 0.5
        self.show_backdrop_init = bpy.context.space_data.show_backdrop
        print("Start")

    def __del__(self):
        print("End")

    def update_time_cursor(self):
        """Updates the position of the time cursor when the preview is active"""
        if not self.show_preview:
            return False

        active = bpy.context.scene.sequence_editor.active_strip
        cursor_pos = active.frame_final_start + \
            floor(active.frame_final_duration * self.preview_ratio)
        bpy.context.scene.frame_set(cursor_pos)
        return True

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            self.last_frame = self.frame
            self.frame = context.region.view2d.region_to_view(
                x=event.mouse_region_x,
                y=event.mouse_region_y)[0]
            offset = self.frame - self.last_frame

            if self.seq_1.frame_final_duration + offset - self.crossfade_duration > 1 and \
               self.seq_2.frame_final_duration - offset - self.crossfade_duration > 1:
                bpy.ops.transform.seq_slide(
                    value=(self.frame - self.last_frame, 0))
            self.update_time_cursor()
        elif event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'ESC'}:
            if self.show_preview:
                context.scene.frame_set(self.time_cursor_init_frame)
                bpy.context.space_data.show_backdrop = self.show_backdrop_init
            if event.type == 'LEFTMOUSE':
                return {"FINISHED"}
            elif event.type in {'RIGHTMOUSE', 'ESC'}:
                return {'CANCELLED'}

        # Preview frame and backdrop toggle
        if event.value == 'PRESS':
            if event.type in {'LEFT_ARROW', 'A'}:
                self.preview_ratio = max(self.preview_ratio - 0.5, 0)
                self.update_time_cursor()
            elif event.type in {'RIGHT_ARROW', 'D'}:
                self.preview_ratio = min(self.preview_ratio + 0.5, 1)
                self.update_time_cursor()
            elif event.type == 'P':
                self.show_preview = True if not self.show_preview else False
                bpy.context.space_data.show_backdrop = self.show_preview
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if not context.area.type == 'SEQUENCE_EDITOR':
            self.report({
                'WARNING'
            }, "You need to be in the Video Sequence Editor to use this tool. \
                        Operation cancelled.")
            return {'CANCELLED'}

        active = bpy.context.scene.sequence_editor.active_strip

        if active.type != "GAMMA_CROSS":
            self.report({
                'WARNING'
            }, "The active strip has to be a gamma cross for this tool to work. \
                        Operation cancelled.")
            return {"CANCELLED"}

        self.seq_1, self.seq_2 = active.input_1, active.input_2
        self.crossfade_duration = active.frame_final_duration

        bpy.ops.sequencer.select_all(action='DESELECT')
        active.select = True
        active.input_1.select_right_handle = True
        active.input_2.select_left_handle = True
        active.input_1.select = True
        active.input_2.select = True

        self.frame = context.region.view2d.region_to_view(
            x=event.mouse_region_x,
            y=event.mouse_region_y)[0]

        if self.show_preview:
            bpy.context.space_data.show_backdrop = True
        # self.mouse_path = []
        # args = (self, context)
        # self._handle = bpy.types.SpaceSequenceEditor.draw_handler_add(
        #     draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

# def draw_callback_px(self, context):
#     # print("mouse points", len(self.mouse_path))

#     region = context.region
#     active = context.scene.sequence_editor.active_strip
#     if active is None:
#         return

#     x = active.frame_final_start
#     y = active.channel
#     x, y = region.view2d.view_to_region(x, y)

#     font_id = 0  # XXX, need to find out how best to get this.
#     blf.position(font_id, x, y, 0)
#     blf.size(font_id, 20, 72)
#     # region_to_view gives the region coords.  x is frame, y is channel.
#     x, y = region.view2d.region_to_view(*self.mouse_path[-1])
#     blf.draw(font_id, "Hello Word %d %d" % (x, y))
#     context.scene.frame_set(x)
