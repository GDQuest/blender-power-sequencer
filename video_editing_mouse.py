"""Video editing tools for Blender using the mouse"""
from math import floor, sqrt

import bpy
from bpy.props import BoolProperty, IntProperty, EnumProperty, FloatProperty, StringProperty
from .functions.sequences import find_strips_mouse, find_effect_strips, get_frame_range
from operator import attrgetter
# import blf


def find_snap_candidate(frame=0):
    """
    Finds and returns the best frame snap candidate around the frame
    """
    closest_cut_frame = 1000000
    for s in bpy.context.sequences:
        start_to_frame = frame - s.frame_final_start
        end_to_frame =  frame - s.frame_final_end
        distance_to_start = abs( start_to_frame )
        distance_to_end = abs(end_to_frame)
        smallest_distance = min(distance_to_start, distance_to_end)

        if smallest_distance == distance_to_start:
            snap_candidate = frame - start_to_frame
        else:
            snap_candidate = frame - end_to_frame

        if abs(frame - snap_candidate) < abs(frame - closest_cut_frame):
            closest_cut_frame = snap_candidate
    return closest_cut_frame


# FIXME: 122, "sorted_sequences = sorted(bpy.context.selected_sequences, key=attrgetter('frame_final_start'))[0]"
# If trimming the start of the first sequence, there's no sequence selected. https://github.com/GDquest/GDquest-VSE/issues/1
class MouseCut(bpy.types.Operator):
    """Cuts, trims and remove gaps with mouse clicks"""
    bl_idname = "power_sequencer.mouse_cut"
    bl_label = "PS.Mouse cut strips"
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
    select_linked = BoolProperty(
        name="Use linked time",
        description=
        "In mouse or smart mode, always cut linked strips if this is checked",
        default=False)
    remove_gaps = BoolProperty(
        name="Remove gaps",
        description="When trimming the sequences, remove gaps automatically",
        default=False)
    cut_gaps = BoolProperty(
        name="Cut gaps",
        description="If you click on a gap, remove it",
        default=True)

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
    threshold_trim_distance = IntProperty(
        name="Tablet trim distance",
        description="If you use a pen tablet, the trim will only happen past this distance",
        default=6,
        min=0)

    use_pen_tablet = False
    mouse_start_x, mouse_start_y = 0.0, 0.0

    start_frame, start_channel = 0, 0
    end_frame, end_channel = 0, 0
    select_mouse, action_mouse = '', ''
    cut_mode = ''

    @classmethod
    def poll(cls, context):
        return context.sequences is not None

    def invoke(self, context, event):
        # Detect pen tablets
        if event.pressure not in [0.0, 1.0]:
            self.use_pen_tablet = True
            self.mouse_start_x, self.mouse_start_y = event.mouse_region_x, event.mouse_region_y

        frame_float, channel_float = context.region.view2d.region_to_view(
            x=event.mouse_region_x,
            y=event.mouse_region_y)
        self.start_frame, self.start_channel = round(frame_float), floor(channel_float)
        self.end_frame = self.start_frame

        # Reverse keymaps if the user selects with the left mouse button
        self.select_mouse = 'RIGHTMOUSE'
        self.action_mouse = 'LEFTMOUSE'
        if bpy.context.user_preferences.inputs.select_mouse == 'LEFT':
            self.select_mouse = 'LEFTMOUSE'
            self.action_mouse = 'RIGHTMOUSE'


        bpy.context.scene.frame_current = self.start_frame
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


    def modal(self, context, event):
        # if event.type in {'LEFTMOUSE', 'RIGHTMOUSE'}:
        #     print('type: {!s}, value: {!s}'.format(event.type, event.value))
        if event.type in {'ESC'}:
            return {'CANCELLED'}

        elif event.type == self.action_mouse and event.value == 'RELEASE':
            self.select_mode = 'cursor' if event.shift else 'smart'

            cursor_distance = abs(event.mouse_region_x - self.mouse_start_x)
            if (self.use_pen_tablet and cursor_distance <= self.threshold_trim_distance) \
               or self.start_frame == self.end_frame:
                to_select = self.find_strips_to_select(self.start_frame, self.start_channel)
                bpy.ops.sequencer.select_all(action='DESELECT')
                for s in to_select:
                    s.select = True
                self.cut_strips_or_gap()
            else:
                bpy.ops.power_sequencer.mouse_trim(start_frame=self.start_frame, end_frame=self.end_frame, select_mode='cursor')
            return {'FINISHED'}

        elif event.type == 'MOUSEMOVE':
            x, y = context.region.view2d.region_to_view(
                x=event.mouse_region_x,
                y=event.mouse_region_y)
            self.end_frame, self.end_channel = round(x), floor(y)
            bpy.context.scene.frame_current = self.end_frame
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}


    def find_strips_to_select(self, start_frame, start_channel):
        """
        Finds and Returns the strips to cut or trim
        """
        strips_to_select = []
        overlapping_strips = find_strips_mouse(start_frame, start_channel, self.select_linked)

        if self.select_mode in ('mouse', 'smart'):
            if overlapping_strips:
                strips_to_select.extend(overlapping_strips)
            elif self.select_mode == 'mouse':
                return None

        if self.select_mode == 'cursor' or (not overlapping_strips and self.select_mode == 'smart'):
            for s in bpy.context.sequences:
                if s.frame_final_start <= start_frame <= s.frame_final_end:
                    strips_to_select.append(s)
        return strips_to_select


    def cut_strips_or_gap(self):
        if self.cut_gaps and len(bpy.context.selected_sequences) == 0:
            bpy.ops.sequencer.gap_remove(all=False)
        else:
            bpy.ops.sequencer.cut(frame=bpy.context.scene.frame_current, type='SOFT', side='BOTH')


class MouseTrim(bpy.types.Operator):
    """
    Trims a frame range or a selection from a start to an end frame.
    If there's no precise time range, auto trims based on the closest cut

    Args:
    - start_frame and end_frame (int) define the frame range to trim
    """
    bl_idname = "power_sequencer.mouse_trim"
    bl_label = "PS.Mouse trim strips"
    bl_options = {'REGISTER', 'UNDO'}


    select_mode = EnumProperty(
        items=[('mouse', 'Mouse', 'Only select the strip hovered by the mouse'),
               ('cursor', 'Time cursor', 'Select all of the strips the time cursor overlaps'),
               ('smart', 'Smart', 'Uses the selection if possible, else uses the other modes')],
        name="Selection mode",
        description= "Auto-select the strip you click on or that the time cursor overlaps",
        default='smart')
    select_linked = BoolProperty(
        name="Use linked time",
        description= "If auto-select, cut linked strips if checked",
        default=False)
    remove_gaps = BoolProperty(
        name="Remove gaps",
        description="When trimming the sequences, remove gaps automatically",
        default=True)
    start_frame, end_frame = IntProperty(), IntProperty()
    to_select = []

    @classmethod
    def poll(cls, context):
        return context.sequences is not None

    def execute(self, context):
        # print('start: {}, end: {}'.format(self.start_frame, self.end_frame))

        trim_start = self.start_frame if self.start_frame <= self.end_frame else self.end_frame
        trim_end = self.end_frame if self.end_frame >= self.start_frame else self.start_frame
        strips_to_delete, strips_to_trim = find_strips_in_range(trim_start, trim_end)
        for s in strips_to_trim:
            if self.select_mode in ('smart', 'mouse') and s not in self.to_select:
                continue
            if s.frame_final_start < trim_start and s.frame_final_end > trim_end:
                bpy.ops.sequencer.select_all(action='DESELECT')
                s.select = True
                bpy.ops.sequencer.cut(frame=trim_start, type='SOFT', side='RIGHT')
                bpy.ops.sequencer.cut(frame=trim_end, type='SOFT', side='LEFT')
                strips_to_delete.append(bpy.context.selected_sequences[0])
                continue
            elif s.frame_final_start < trim_end and s.frame_final_end > trim_end:
                s.frame_final_start = trim_end
            elif s.frame_final_end > trim_start and s.frame_final_start < trim_start:
                s.frame_final_end = trim_start

        bpy.ops.sequencer.select_all(action='DESELECT')
        for s in strips_to_delete:
            s.select = True
        bpy.ops.sequencer.delete()

        if self.remove_gaps:
            bpy.context.scene.frame_current = self.end_frame - 1
            bpy.ops.sequencer.gap_remove()
        return {'FINISHED'}


    def invoke(self, context, event):
        # Snap to closest cut
        # if self.snap_to_closest_cut:
        #     self.start_frame = find_snap_candidate(self.start_frame)
        #     print("old {!s} / new {!s}".format(old_frame, frame))

        if not self.start_frame or self.end_frame:
            bpy.ops.sequencer.select_all(action='DESELECT')

            x, y = context.region.view2d.region_to_view(
                x=event.mouse_region_x,
                y=event.mouse_region_y)
            frame, channel = round(x), floor(y)
            self.to_select = find_strips_mouse(frame, channel, self.select_linked)

            if self.select_mode in ('mouse', 'smart'):
                if self.to_select:
                    for s in self.to_select:
                        s.select = True
                elif self.select_mode == 'mouse':
                    return {"CANCELLED"}
            if self.select_mode == 'cursor' or (not self.to_select and self.select_mode == 'smart'):
                for s in bpy.context.sequences:
                    if s.frame_final_start <= frame <= s.frame_final_end:
                        s.select = True

            selection_start, selection_end = get_frame_range(bpy.context.selected_sequences)
            self.start_frame = frame
            self.end_frame = selection_end if abs(self.start_frame - selection_end) <= abs(self.start_frame - selection_start) else selection_start
        self.execute(context)
        return {'FINISHED'}



def find_strips_in_range(start_frame, end_frame, sequences = None, find_overlapping = True):
    """
    Returns strips which start and end within a certain frame range, or that overlap a certain frame range
    Args:
    - start_frame, the start of the frame range
    - end_frame, the end of the frame range
    - sequences (optional): only work with these sequences. If it doesn't receive any, the function works with all the sequences in the current context
    - find_overlapping (optional): find and return a list of strips that overlap the frame range

    Returns a tuple of two lists:
    [0], strips entirely in the frame range
    [1], strips that only overlap the frame range
    """
    strips_in_range = []
    strips_overlapping_range = []
    if not sequences:
        sequences = bpy.context.sequences
    for s in sequences:
        if start_frame <= s.frame_final_start <= end_frame:
            if start_frame <= s.frame_final_end <= end_frame:
                strips_in_range.append(s)
            elif find_overlapping:
                strips_overlapping_range.append(s)
        elif find_overlapping and start_frame <= s.frame_final_end <= end_frame:
            strips_overlapping_range.append(s)
        if s.frame_final_start < start_frame and s.frame_final_end > end_frame:
            strips_overlapping_range.append(s)
    return strips_in_range, strips_overlapping_range


def find_closest_surrounding_cuts(frame=0):
    """
    Returns a tuple of (left_cut_frame, right_cut_frame) of the two closest cuts surrounding a frame
    Args:
    - frame, find the closest cuts that surround this frame
    """
    start_cut_frame, end_cut_frame = 1000000, 1000000
    for s in bpy.context.sequences:
        distance_to_start = abs(frame - s.frame_final_start)
        distance_to_end = abs(frame - s.frame_final_end)

        distance_to_start_cut_frame = abs(start_cut_frame - frame)
        distance_to_end_cut_frame = abs(end_cut_frame - frame)

        if s.frame_final_start < frame and \
           distance_to_start < distance_to_start_cut_frame:
            start_cut_frame = s.frame_final_start
        if s.frame_final_end < frame and \
           distance_to_end < distance_to_start_cut_frame:
            start_cut_frame = s.frame_final_end
        if s.frame_final_end > frame and \
           distance_to_end < distance_to_end_cut_frame:
            end_cut_frame = s.frame_final_end
        if s.frame_final_start > frame and \
           distance_to_start < distance_to_end_cut_frame:
            end_cut_frame = s.frame_final_start
    return start_cut_frame, end_cut_frame


def find_cut_and_handles_closest_to_mouse(mouse_x, mouse_y):
    """
    takes the mouse's coordinates in the sequencer area and returns the two strips
    who share the cut closest to the mouse, or the strip with the closest handle.
    Use it to find the handle(s) to select with the grab on the fly operator
    """
    view2d = bpy.context.region.view2d

    closest_cut = (None, None)
    distance_to_closest_cut = 1000000.0

    for s in bpy.context.sequences:
        channel_offset = s.channel + 0.5
        start_x, start_y = view2d.view_to_region(s.frame_final_start, channel_offset)
        end_x, end_y = view2d.view_to_region(s.frame_final_start, channel_offset)

        distance_to_start = calculate_distance(start_x, start_y, mouse_x, mouse_y)
        distance_to_end = calculate_distance(end_x, end_y, mouse_x, mouse_y)

        if distance_to_start < distance_to_closest_cut:
            closest_cut = (start_x, start_y)
            distance_to_closest_cut = distance_to_start
        if distance_to_end < distance_to_closest_cut:
            closest_cut = (end_x, end_y)
            distance_to_closest_cut = distance_to_end

    closest_cut_local_coords = view2d.region_to_view(closest_cut[0], closest_cut[1])
    frame, channel = round(closest_cut_local_coords[0]), floor(closest_cut_local_coords[1])
    return frame, channel


def calculate_distance(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


class GrabClosestHandleOrCut(bpy.types.Operator):
    """
    Selects and grabs the strip handle or cut closest to the mouse cursor.
    Hover near a cut and fire this tool to slide it.
    """
    bl_idname = "power_sequencer.grab_closest_handle_or_cut"
    bl_label = "PS.Grab closest handle or cut"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context is not None

    def invoke(self, context, event):
        if not bpy.context.sequences:
            return {'CANCELLED'}

        sequencer = bpy.ops.sequencer
        view2d = bpy.context.region.view2d

        mouse_x, mouse_y = event.mouse_region_x, event.mouse_region_y
        frame, channel = find_cut_and_handles_closest_to_mouse(mouse_x, mouse_y)

        matching_sequences = []
        for s in bpy.context.sequences:
            if s.channel == channel:
                if abs(s.frame_final_start - frame) <= 1 or abs(s.frame_final_end - frame) <= 1:
                    matching_sequences.append(s)
        matching_count = len(matching_sequences)

        sequencer.select_all(action='DESELECT')
        if matching_count == 1:
            sequence = matching_sequences[0]
            sequence.select = True
            if abs(sequence.frame_final_start - frame) <= 1:
                sequence.select_left_handle = True
            elif abs(sequence.frame_final_end - frame) <= 1:
                sequence.select_right_handle = True
        elif matching_count == 2:
            cut_select_range = 40
            sorted_sequences = sorted(matching_sequences, key=attrgetter('frame_final_start'))
            first_sequence, second_sequence = sorted_sequences[0], sorted_sequences[1]

            cut_x, _ = view2d.view_to_region(frame, channel)
            if abs(mouse_x - cut_x) > cut_select_range:
                if mouse_x < cut_x:
                    first_sequence.select = True
                    first_sequence.select_right_handle = True
                else:
                    second_sequence.select = True
                    second_sequence.select_left_handle = True
            else:

                first_sequence.select = True
                first_sequence.select_right_handle = True
                second_sequence.select = True
                second_sequence.select_left_handle = True
        bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
        return {'FINISHED'}


class TrimToSurroundingCuts(bpy.types.Operator):
    """
    Find the two closest cuts, trims and deletes all strips above in the range but leaves some margin. Removes the newly formed gap.
    """
    bl_idname = "power_sequencer.trim_to_surrounding_cuts"
    bl_label = "PS.Trim to surrounding cuts"
    bl_options = {'REGISTER', 'UNDO'}

    margin = FloatProperty(
        name="Trim margin",
        description=
        "Margin to leave on either sides of the trim in seconds",
        default=0.2,
        min=0)
    remove_gaps = BoolProperty(
        name="Remove gaps",
        description="When trimming the sequences, remove gaps automatically",
        default=True)

    @classmethod
    def poll(cls, context):
        return context is not None

    def invoke(self, context, event):
        if not bpy.context.sequences:
            return {'CANCELLED'}

        sequencer = bpy.ops.sequencer
        time_cursor_start_frame = bpy.context.scene.frame_current

        # Convert mouse position to frame, channel
        x, y = context.region.view2d.region_to_view(
            x=event.mouse_region_x,
            y=event.mouse_region_y)
        frame, channel = round(x), floor(y)

        left_cut_frame, right_cut_frame = find_closest_surrounding_cuts(frame)
        surrounding_cut_frames_duration = abs(left_cut_frame - right_cut_frame)

        margin_frame = round(self.margin * bpy.context.scene.render.fps)

        if surrounding_cut_frames_duration <= margin_frame * 2:
            self.report({'WARNING'}, "The trim margin is larger than the gap \n Use snap trim or reduce the margin")
            return {'CANCELLED'}

        strips_to_delete, strips_to_trim = find_strips_in_range(left_cut_frame, right_cut_frame)
        trim_start, trim_end = left_cut_frame + margin_frame, right_cut_frame - margin_frame

        # print("start: {!s}, end: {!s}".format(left_cut_frame, right_cut_frame))
        # for s in strips_to_trim:
        #     print(s.name)

        for s in strips_to_trim:
            # If the strip is larger than the range to trim cut it in three
            if s.frame_final_start < trim_start and s.frame_final_end > trim_end:
                sequencer.select_all(action='DESELECT')
                s.select = True
                sequencer.cut(frame=trim_start, type='SOFT', side='RIGHT')
                sequencer.cut(frame=trim_end, type='SOFT', side='LEFT')
                strips_to_delete.append(bpy.context.selected_sequences[0])
                continue

            if s.frame_final_start < trim_end and s.frame_final_end > trim_end:
                s.frame_final_start = trim_end
            elif s.frame_final_end > trim_start and s.frame_final_start < trim_start:
                s.frame_final_end = trim_start


        # Delete all sequences that are between the cuts
        sequencer.select_all(action='DESELECT')
        for s in strips_to_delete:
            s.select = True
        sequencer.delete()


        if self.remove_gaps:
            frame_to_remove_gap = right_cut_frame - 1 if frame == right_cut_frame else frame
            # bpy.ops.anim.change_frame(frame_to_remove_gap)
            bpy.context.scene.frame_current = frame_to_remove_gap
            sequencer.gap_remove()
            bpy.context.scene.frame_current = trim_start
        return {'FINISHED'}


class MouseToggleMute(bpy.types.Operator):
    """Toggle mute a sequence as you click on it"""
    bl_idname = "power_sequencer.mouse_toggle_mute"
    bl_label = "PS.Toggle Mute with Mouse"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context is not None

    def invoke(self, context, event):
        sequencer = bpy.ops.sequencer

        # get current frame and channel the mouse hovers
        x, y = context.region.view2d.region_to_view(
            x=event.mouse_region_x,
            y=event.mouse_region_y)
        frame, channel = round(x), floor(y)

        # Strip selection
        sequencer.select_all(action='DESELECT')
        to_select = find_strips_mouse(frame, channel)

        if not to_select:
            return {"CANCELLED"}

        for s in to_select:
            s.mute = not s.mute
        return {"FINISHED"}


class EditCrossfade(bpy.types.Operator):
    """
    Selects handles of a crossfade strip's input and calls the grab operator
    """
    bl_idname = "power_sequencer.edit_crossfade"
    bl_label = "PS.Edit crossfade"
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
