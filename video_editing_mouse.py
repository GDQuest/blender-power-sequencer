"""Video editing tools for Blender using the mouse"""
from math import floor

import bpy
from bpy.props import BoolProperty, IntProperty, EnumProperty
from .functions.sequences import find_strips_mouse, find_effect_strips, get_frame_range
from operator import attrgetter
# import blf


# TODO: in cursor mode, if trim, if there's a strip that's smaller than
# the part that's been cut, delete it
# Look at selected strips closest side and cut frame
# if any strip on other channels between those frames and smaller, delete it
class MouseCut(bpy.types.Operator):
    """Cuts the strip sitting under the mouse"""
    bl_idname = "gdquest_vse.mouse_cut"
    bl_label = "Mouse cut strips"
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
    cut_mode = EnumProperty(items=[('cut', 'Cut', 'Cut the strips'), (
        'trim', 'Trim', 'Trim the selection')],
                            name='Cut mode',
                            description='Cut or trim the selection',
                            default='cut')
    remove_gaps = BoolProperty(
        name="Remove gaps",
        description="When trimming the sequences, remove gaps automatically",
        default=False)
    auto_move_cursor = BoolProperty(
        name="Auto move cursor",
        description=
        "When trimming the sequence, auto move the cursor if playback is active",
        default=True)
    cursor_offset = IntProperty(
        name="Cursor trim offset",
        description=
        "On trim, during playback, offset the cursor to better see if the cut works",
        default=12,
        min=0)
    select_linked = BoolProperty(
        name="Use linked time",
        description=
        "In mouse or smart mode, always cut linked strips if this is checked",
        default=False)

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
        sequencer.select_all(action='DESELECT')
        to_select = find_strips_mouse(frame, channel, self.select_linked)

        if select_mode in ('mouse', 'smart'):
            if to_select:
                for s in to_select:
                    s.select = True
            elif select_mode == 'mouse':
                return {"CANCELLED"}

        if select_mode == 'cursor' or (not to_select and select_mode == 'smart'):
            for s in bpy.context.sequences:
                if s.frame_final_start <= frame <= s.frame_final_end:
                    s.select = True

        # Cut and trim
        if self.cut_mode == 'cut':
            sequencer.cut(frame=bpy.context.scene.frame_current,
                          type='SOFT',
                          side='BOTH')
        elif self.cut_mode == 'trim':
            start, end = get_frame_range(bpy.context.selected_sequences)

            # Find strips to delete
            to_delete = []
            delete_start, delete_end = 0, 0
            if abs(frame - start) <= abs(start - end) / 2:
                delete_start = start
                delete_end = frame
            else:
                delete_start = frame
                delete_end = end
            for s in bpy.context.sequences:
                if delete_start <= s.frame_final_start <= delete_end and delete_start <= s.frame_final_end <= delete_end:
                    to_delete.append(s)

            # Trim and delete strips
            bpy.ops.gdquest_vse.smart_snap(side='auto')
            sequencer.select_all(action='DESELECT')
            for s in to_delete:
                s.select = True
            sequencer.delete()

            if self.remove_gaps:
                anim.change_frame(frame=frame - 1)
                sequencer.gap_remove()

            # Move time cursor back
            if self.auto_move_cursor and bpy.context.screen.is_animation_playing:
                first_seq = sorted(bpy.context.selected_sequences,
                                   key=attrgetter('frame_final_start'))[0]
                frame = first_seq.frame_final_start - self.cursor_offset \
                    if abs(frame - first_seq.frame_final_start) < first_seq.frame_final_duration / 2 \
                    else frame
                anim.change_frame(frame=frame)

        sequencer.select_all(action='DESELECT')
        return {"FINISHED"}


# FIXME: Currently using seq_slide to move the sequences but creates bugs
#        Check how builtin modal operators work instead
# TODO: Store starting frame of the strips and revert to it on CANCELLED
class EditCrossfade(bpy.types.Operator):
    """
    Selects handles to edit crossfade and gives a preview of the fade point.
    """
    bl_idname = "gdquest_vse.edit_crossfade"
    bl_label = "Edit crossfade"
    bl_options = {'REGISTER', 'UNDO'}

    show_preview = BoolProperty(
        name="Preview the crossfade",
        description=
        "Gives a preview of the crossfade sides, but can affect performances",
        default=False)

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
        """
        Updates the position of the time cursor when the preview is active
        """
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
                # TODO: Replace with moving the actual strip handles
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
                # TODO: Revert back to original position
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
                        Operation cancelled."
                                             )
            return {'CANCELLED'}

        active = bpy.context.scene.sequence_editor.active_strip

        if active.type != "GAMMA_CROSS":
            effect = find_effect_strips(active)
            if effect is None:
                self.report({
                    'WARNING'
                }, "The active strip has to be a gamma cross for this tool to work. \
                            Operation cancelled."
                                                 )
                return {"CANCELLED"}
            active = bpy.context.scene.sequence_editor.active_strip = effect[0]

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
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
