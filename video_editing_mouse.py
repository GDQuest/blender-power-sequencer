"""Video editing tools for Blender using the mouse"""
from math import floor

import bpy
from bpy.props import BoolProperty, IntProperty, EnumProperty
from .functions.sequences import find_strips_mouse, find_effect_strips, get_frame_range
from operator import attrgetter
# import blf


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

            print(end)

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


class EditCrossfade(bpy.types.Operator):
    """
    Selects handles to edit crossfade
    """
    bl_idname = "gdquest_vse.edit_crossfade"
    bl_label = "Edit crossfade"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.area.type == 'SEQUENCE_EDITOR':
            self.report({'WARNING'}, "You need to be in the Video Sequence Editor to use this tool. \
                        Operation cancelled.")
            return {'CANCELLED'}

        active = bpy.context.scene.sequence_editor.active_strip

        if active.type != "GAMMA_CROSS":
            effect = find_effect_strips(active)
            if effect is None:
                self.report({'WARNING'},
                            "The active strip has to be a gamma cross for this tool to work. \
                            Operation cancelled.")
                return {"CANCELLED"}
            active = bpy.context.scene.sequence_editor.active_strip = effect[0]

        bpy.ops.sequencer.select_all(action='DESELECT')
        active.select = True
        active.input_1.select_right_handle = True
        active.input_2.select_left_handle = True
        active.input_1.select = True
        active.input_2.select = True

        bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
        return {'FINISHED'}
