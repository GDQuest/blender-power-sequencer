import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty, EnumProperty
from operator import attrgetter

from .functions.global_settings import SequenceTypes, SearchMode
from .functions.sequences import find_next_sequences, \
    select_strip_handle, slice_selection, get_frame_range, \
    find_linked, is_in_range, set_preview_range, filter_sequences_by_type

# ---------------- Operators -----------------------
# --------------------------------------------------
# TODO: Make it work with 2+ selected strips
# TODO: make it work with pictures and transform strips
# TODO: If source strip has a special blending mode, use that for crossfade?
# TODO: make sure there's no effect on the strip?
# IDEA: If crossfade between effect strips or 2 pictures, set crossfade strip
# ALPHA_OVER
# IDEA: Add custom property to store the name/data_path of the GAMMA_CROSS
# effect added to both strips, so we can detect it later. Why?
class AddCrossfade(bpy.types.Operator):
    """
    Based on the active strip, finds the closest next sequence
    of a similar type, moves it so it overlaps the active strip,
    and adds a gamma_cross effect between them.
    Works with MOVIE, IMAGE and META strips
    """
    bl_idname = "power_sequencer.add_crossfade"
    bl_label = "PS.Add Crossfade"
    bl_description = "Adds a Gamma Cross fade layer effect between \
                      the selected layer and the closest one to its right."

    bl_options = {"REGISTER", "UNDO"}

    crossfade_length = IntProperty(
        name="Crossfade length",
        description="Length of the crossfade in frames",
        default=10,
        min=1)
    force_length = BoolProperty(
        name="Force crossfade length",
        description="When true, moves the second strip so the crossfade \
                     is of the length set in 'Crossfade Length'"
        , default=True)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        selection = bpy.context.selected_sequences

        if not len(selection) == 1:
            self.report({"ERROR_INVALID_INPUT"}, "Select a single strip to \
            crossfade from"
                           )
            return {"CANCELLED"}

        active = bpy.context.scene.sequence_editor.active_strip
        selection = filter_sequences_by_type(selection, SequenceTypes.VIDEO,
                                             SequenceTypes.IMAGE)
        if not selection:
            self.report({"ERROR_INVALID_INPUT"},
                        "Please select a movie, meta or image strip")
            return {"CANCELLED"}
        if selection[0] != active:
            bpy.context.scene.sequence_editor.active_strip = \
                active = selection[0]

        # Find the best strip after active in timeline to crossfade to
        next_sequences = find_next_sequences(selection)
        next_sequences = filter_sequences_by_type(
            next_sequences, SequenceTypes.VIDEO, SequenceTypes.IMAGE)
        if not next_sequences:
            return {"CANCELLED"}
        threshold = active.channel - 1
        higher_sequences = [s
                            for s in next_sequences
                            if s.channel >= threshold]
        priority_neighbors = [s
                              for s in higher_sequences
                              if s.frame_final_start >= active.frame_final_end
                              and s.channel - active.channel in (-1, 0, 1)]
        if priority_neighbors:
            neighbor = min(priority_neighbors,
                           key=attrgetter('frame_final_start', 'channel'))
        elif higher_sequences:
            neighbor = min(higher_sequences,
                           key=attrgetter('channel', 'frame_final_start'))
        else:
            lower_sequences = [s
                               for s in next_sequences
                               if s.channel < threshold]
            neighbor = min(lower_sequences,
                           key=attrgetter('channel', 'frame_final_start'))

        if self.force_length:
            frame_offset = neighbor.frame_final_start - active.frame_final_end
            neighbor.frame_start -= frame_offset
            neighbor.frame_final_start -= self.crossfade_length
        active.select = True
        neighbor.select = True
        bpy.context.scene.sequence_editor.active_strip = neighbor
        sequencer.effect_strip_add(type='GAMMA_CROSS')
        return {"FINISHED"}


# FIXME: bug if selecting effect strips
# TODO: If single strip, use the full source so you can slide it?
# TODO: if speed already applied, update speed?
# Means need function to unspeed and redo?
class AddSpeed(bpy.types.Operator):
    bl_idname = "power_sequencer.speed_up_sequence"
    bl_label = "PS.Speed up Sequence"
    bl_description = "Adds a speed effect to your clip, sets its speed and \
        size, wraps it into a meta strip set to over drop for easier editing"

    bl_options = {"REGISTER", "UNDO"}

    speed_factor = IntProperty(
        name="Speed factor",
        description="How many times the footage gets sped up",
        default=2,
        min=0)
    individual_sequences = BoolProperty(
        name="Affect individual strips",
        description="Speed up every VIDEO strip individually",
        default=False)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        scene = bpy.context.scene
        active = scene.sequence_editor.active_strip

        # Select linked sequences
        for s in find_linked(bpy.context.selected_sequences):
            s.select = True
        selection = bpy.context.selected_sequences

        video_sequences = [s for s in selection
                           if s.type in SequenceTypes.VIDEO]

        if not video_sequences:
            self.report({
                "ERROR_INVALID_INPUT"
            }, "No Movie sequence or Metastrips selected. Operation cancelled")
            return {"CANCELLED"}

        # Slice the selection
        selection_blocks = []
        if self.individual_sequences:
            for s in selection:
                if s.type in SequenceTypes.EFFECT:
                    self.report({
                        "ERROR_INVALID_INPUT"
                    }, "Can't speed up individual sequences if effect strips \
                    are selected. Please only select VIDEO or META strips. \
                    Operation cancelled"
                                        )
                    return {'CANCELLED'}
            selection_blocks = [[s] for s in video_sequences]
        else:
            selection_blocks = slice_selection(selection)

        for block in selection_blocks:
            start, end = 0, 0
            sequencer.select_all(action='DESELECT')
            if len(block) == 1:
                active = scene.sequence_editor.active_strip = block[0]
                # TODO: Use the full source clip
                # start = active.frame_final_start / self.speed_factor
                # end = start + active.frame_final_duration / self.speed_factor
                # active.frame_offset_start, active.frame_offset_end = 0, 0
            else:
                for s in block:
                    s.select = True
                # SELECT GROUPED ONLY AFFECTS ACTIVE STRIP
                # bpy.ops.sequencer.select_grouped(type='EFFECT_LINK')
                sequencer.meta_make()
                active = scene.sequence_editor.active_strip
            # Add speed effect
            sequencer.effect_strip_add(type='SPEED')
            effect_strip = bpy.context.scene.sequence_editor.active_strip
            effect_strip.use_default_fade = False
            effect_strip.speed_factor = self.speed_factor

            sequencer.select_all(action='DESELECT')
            active.select_right_handle = True
            active.select = True
            scene.sequence_editor.active_strip = active
            source_name = active.name

            from math import ceil
            size = ceil(active.frame_final_duration /
                        effect_strip.speed_factor)
            endFrame = active.frame_final_start + size
            sequencer.snap(frame=endFrame)

            effect_strip.select = True
            sequencer.meta_make()
            bpy.context.selected_sequences[0].name = source_name + " " + str(
                self.speed_factor) + 'x'
        self.report({"INFO"}, "Successfully processed " +
                    str(len(selection_blocks)) + " selection blocks")
        return {"FINISHED"}


class SelectLinkedEffect(bpy.types.Operator):
    bl_idname = 'power_sequencer.find_linked_effect'
    bl_label = 'PS.Select linked effect'
    bl_description = 'Select all strips that are linked by an effect strip'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for s in find_linked(bpy.context.selected_sequences):
            s.select = True
        return {'FINISHED'}


class ConcatenateStrips(bpy.types.Operator):
    """
    Concatenates selected strips (removes space between them)
    If a single strip is selected, finds all the strips after it in the channel
    """
    bl_idname = "power_sequencer.concatenate_strips"
    bl_label = "PS.Concatenate strips"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sequences = bpy.context.selected_sequences

        # If only 1 sequence selected, find next sequences in channel
        if len(sequences) == 1:
            in_channel = [s
                          for s in find_next_sequences(sequences)
                          if s.channel == sequences[0].channel]
            for s in in_channel:
                sequences.append(s)
        sequences = filter_sequences_by_type(sequences, SequenceTypes.VIDEO,
                                             SequenceTypes.IMAGE,
                                             SequenceTypes.SOUND)

        if len(sequences) <= 1:
            self.report({"INFO"}, "No strips to concatenate.")
            return {'CANCELLED'}

        channels = list(set([s.channel for s in sequences]))
        sequences = sorted(sequences,
                           key=attrgetter('channel', 'frame_final_start'))
        # Concatenate the channels
        for channel in channels:
            concat_start = 0
            concat_sequences = [s for s in sequences if s.channel == channel]
            concat_start = concat_sequences[0].frame_final_end
            concat_sequences.pop(0)

            for s in concat_sequences:
                gap = s.frame_final_start - concat_start
                s.frame_start -= gap
                concat_start += s.frame_final_duration
        return {"FINISHED"}


class SelectShortStrips(bpy.types.Operator):
    bl_idname = "power_sequencer.select_short_strips"
    bl_label = "PS.Select short strips"
    bl_description = "Filters the current selection down to the strips that are \
        less than the 'Max strip length' frames long."

    bl_options = {'REGISTER', 'UNDO'}

    max_strip_length = IntProperty(
        name="Max strip length",
        description="Length of the selected strips in frames",
        default=8,
        min=1)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for s in bpy.context.selected_sequences:
            if s.frame_final_duration > self.max_strip_length:
                s.select = False
        return {"FINISHED"}


class SmartSnap(bpy.types.Operator):
    """Trims, extends and snaps selected strips to cursor"""
    bl_idname = "power_sequencer.smart_snap"
    bl_label = "PS.Smart snap strip handles"
    bl_options = {'REGISTER', 'UNDO'}

    side = EnumProperty(
        items=[('left', 'Left', 'Left side'), ('right', 'Right', 'Right side'),
               ('auto', 'Auto', 'Use the side closest to the time cursor')],
        name="Snap side",
        description="Handle side to use for the snap",
        default='auto')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        current_frame = bpy.context.scene.frame_current

        select_strip_handle(bpy.context.selected_sequences, self.side,
                            current_frame)

        sequencer.snap(frame=current_frame)

        for s in context.selected_sequences:
            s.select_right_handle = False
            s.select_left_handle = False
        return {"FINISHED"}


class GrabStillImage(bpy.types.Operator):
    """Converts image under the cursor to a still image, to create
    a pause effect in the video, using the active sequence"""
    bl_idname = "power_sequencer.grab_still_image"
    bl_label = "PS.Grab still image from active strip"
    bl_options = {'REGISTER', 'UNDO'}

    strip_duration = IntProperty(
        name="Strip length",
        description="Length of the new strip in frames",
        default=106)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = bpy.context.scene
        active = scene.sequence_editor.active_strip
        sequencer = bpy.ops.sequencer
        transform = bpy.ops.transform

        start_frame = scene.frame_current
        offset = self.strip_duration

        if active.type not in SequenceTypes.VIDEO:
            self.report({
                "ERROR_INVALID_INPUT"
            }, "You must select a video or meta strip. \
                You selected a strip of type"
                                              + str(active.type) + " instead.")
            return {"CANCELLED"}

        if not active.frame_final_start <= start_frame < \
           active.frame_final_end:
            self.report({"ERROR_INVALID_INPUT"},
                        "Your time cursor must be on the frame you want \
                        to convert to a still image."
                                                     )
            return {"CANCELLED"}

        if start_frame == active.frame_final_start:
            scene.frame_current = start_frame + 1

        active.select = True
        source_blend_type = active.blend_type
        sequencer.cut(frame=scene.frame_current, type='SOFT', side='RIGHT')
        transform.seq_slide(value=(offset, 0))
        sequencer.cut(frame=scene.frame_current + offset + 1,
                      type='SOFT',
                      side='LEFT')
        transform.seq_slide(value=(-offset, 0))

        sequencer.meta_make()
        active = scene.sequence_editor.active_strip
        active.name = 'Still image'
        active.blend_type = source_blend_type
        active.select_right_handle = True
        transform.seq_slide(value=(offset, 0))

        scene.frame_current = start_frame

        active.select = True
        active.select_right_handle = False
        active.select_left_handle = False
        return {"FINISHED"}


class ToggleHidden(bpy.types.Operator):
    bl_idname = 'power_sequencer.toggle_sequences_muted'
    bl_label = 'PS.Toggle sequences muted'
    bl_description = 'Mute or unmute sequences'
    bl_options = {'REGISTER', 'UNDO'}

    use_unselected = BoolProperty(name="Use unselected",
                                  description="Toggle non selected sequences",
                                  default=False)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = bpy.context.selected_sequences

        if self.use_unselected:
            selection = [s for s in bpy.context.sequences
                         if s not in selection]

        if not selection:
            self.report({"WARNING"}, "No sequences to toggle muted")
            return {'CANCELLED'}

        mute = not selection[0].mute
        for s in selection:
            s.mute = mute
        return {'FINISHED'}


class ChannelOffset(bpy.types.Operator):
    bl_idname = 'power_sequencer.channel_offset'
    bl_label = 'PS.Channel offset'
    bl_description = 'Move selected strips up or down a channel'
    bl_options = {'REGISTER', 'UNDO'}

    direction = EnumProperty(items=[
        ('up', 'up', 'Move the selection 1 channel up'), (
            'down', 'down', 'Move the selection 1 channel down')
    ],
                             name='Direction',
                             description='Move the sequences up or down',
                             default='up')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = bpy.context.selected_sequences
        if not selection:
            return {'CANCELLED'}

        selection = sorted(selection,
                           key=attrgetter('channel', 'frame_final_start'))

        if self.direction == 'up':
            for s in reversed(selection):
                s.channel += 1
        elif self.direction == 'down':
            for s in selection:
                if (s.channel > 1):
                    s.channel -= 1
        return {'FINISHED'}


# TODO: find a way to get the selection bounding box and place it
# where there is space for it?
class SnapSelectionToCursor(bpy.types.Operator):
    """Snap selected strips to the cursor, but as a block"""
    bl_idname = "power_sequencer.snap_selection_to_cursor"
    bl_label = "PS.Snap selection to cursor"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = sorted(bpy.context.selected_sequences,
                           key=attrgetter('frame_final_start'))

        time_move = selection[
            0].frame_final_start - bpy.context.scene.frame_current

        from .functions.sequences import find_empty_channel
        empty_channel = find_empty_channel()

        for s in selection:
            if s.type in SequenceTypes.VIDEO or s.type in SequenceTypes.IMAGE or s.type in SequenceTypes.SOUND:
                s.frame_start -= time_move
        return {'FINISHED'}


class BorderSelect(bpy.types.Operator):
    bl_idname = 'power_sequencer.border_select'
    bl_label = 'PS.Border select'
    bl_description = 'Wrapper around Blender\'s border select, \
    deselects handles'
    bl_options = {'REGISTER', 'UNDO'}

    extend = BoolProperty(
        name="Extend the selection",
        description="Extend the current selection if checked, otherwise clear it",
        default=False)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for s in bpy.context.selected_sequences:
            s.select_right_handle = False
            s.select_left_handle = False
        return bpy.ops.sequencer.select_border('INVOKE_DEFAULT', extend=self.extend)


class GrabSequenceHandle(bpy.types.Operator):
    """
    Operator that extends the sequence based on the mouse position.
    If the cursor is to the right of the sequence's middle,
    it moves the right handle.
    If it's on the left side, it moves the left handle.
    """
    bl_idname = 'power_sequencer.grab_sequence_handle'
    bl_label = 'PS.Grab sequence handles'
    bl_description = 'Grabs the sequence\'s handle based on the mouse position'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        selection = bpy.context.selected_sequences
        if not selection:
            return {'CANCELLED'}

        frame, _ = context.region.view2d.region_to_view(
            x=event.mouse_region_x,
            y=event.mouse_region_y)

        bpy.ops.sequencer.select_all(action='DESELECT')
        for s in selection:
            middle = s.frame_final_start + s.frame_final_duration / 2
            if frame >= middle:
                s.select_right_handle = True
            else:
                s.select_left_handle = True
            s.select = True

        bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
        return {'FINISHED'}


class DeselectHandlesAndGrab(bpy.types.Operator):
    """
    Deselect the handles of all selected strips and call the
    Sequence Slide operator
    """
    bl_idname = 'power_sequencer.deselect_handles_seq_slide'
    bl_label = 'PS.Deselect handles and grab'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for s in bpy.context.selected_sequences:
            s.select_left_handle = False
            s.select_right_handle = False
            s.select = True

        bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
        return {'FINISHED'}


class PreviewLastCut(bpy.types.Operator):
    """
    Finds the closest cut to the time cursor and
    sets the preview to a small range around that frame.
    If the preview matches the range, resets to the full timeline
    """
    bl_idname = 'power_sequencer.preview_last_cut'
    bl_label = 'PS.Preview last cut'
    bl_description = 'Toggle preview around the last cut, based on time cursor'
    bl_options = {'REGISTER', 'UNDO'}

    frame_range = IntProperty(name="Preview range",
                              description="Total duration of the preview",
                              default=24,
                              min=1)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = bpy.context.scene
        frame_current = scene.frame_current
        sequences = bpy.context.sequences

        if len(sequences) <= 1:
            return {'CANCELLED'}

        # Find cut closest to time cursor
        last_distance = 100000
        preview_center = 0
        for s in sequences:
            cut = s.frame_final_start
            distance_to_cut = abs(cut - frame_current)
            if distance_to_cut < last_distance:
                last_distance = distance_to_cut
                preview_center = cut

        start = preview_center - self.frame_range / 2
        end = preview_center + self.frame_range / 2
        if preview_center > 1 and start > 1:
            if scene.frame_preview_start == start and scene.frame_preview_end == end:
                start, end = get_frame_range(sequences)
            set_preview_range(start, end)
        return {'FINISHED'}
