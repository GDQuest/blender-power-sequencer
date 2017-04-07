import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty, EnumProperty

from .functions.global_settings import SequenceTypes, SearchMode
from .functions.sequences import find_next_sequences, \
    select_strip_handle, slice_selection, get_frame_range, \
    find_linked, is_in_range, set_preview_range


# ---------------- Operators -----------------------
# --------------------------------------------------
# TODO: Rewrite cleanly
# FIXME: Doesn't work well if there are 3-4-5 channels used. The operator will
# pick strips up to 2 channels below the active one
# TODO: Make it work with 2+ selected strips
# FIXME: Make sure the offset preserves the starting frame of the second strip
# IDEA: make it work with pictures and transform strips
# IDEA: If source strip has a special blending mode, use that for crossfade?
# IDEA: If 2 strips selected and same type familly (visual or sound), crossfade
# from the bottom left one to the top right one
# IDEA: Auto Chain crossfades if more than 2 strips selected?
# IDEA: Add custom properties to the sequences referencing the GAMMA_CROSS
# strip, to easily remove it or process it with Python
# FIXME: Only add new crossfade if there's no existing GAMMA_CROSS between 2
# selected strips
# IDEA: If crossfade between effect strips or 2 pictures, set crossfade strip
# ALPHA_OVER
# IDEA: Add custom property to store the name/data_path of the GAMMA_CROSS
# effect added to both strips, so we can detect it later
# IDEA: The operator should preserve strips with linked times (1 video + 1
# audio)
class AddCrossfade(bpy.types.Operator):
    bl_idname = "gdquest_vse.add_crossfade"
    bl_label = "Add Crossfade"
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
                                                                ,
        default=True)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        active = bpy.context.scene.sequence_editor.active_strip
        selection = bpy.context.selected_sequences

        if not selection:
            return {"CANCELLED"}

        if len(selection) > 1:
            self.report({"ERROR_INVALID_INPUT"}, "Only select one strip to \
            crossfade from"
                           )
            return {"CANCELLED"}

        if active.type not in SequenceTypes.VIDEO:
            if selection[0].type in SequenceTypes.VIDEO:
                bpy.context.scene.sequence_editor.active_strip = \
                    active = selection[0]
            else:
                self.report({"ERROR_INVALID_INPUT"},
                            "You need to select a video \
                sequence to add a crossfade"
                                            )
                return {"CANCELLED"}

        seq = [active, find_next_sequences(SearchMode.NEXT)]
        if not seq[0] and seq[1]:
            self.report({"ERROR_INVALID_INPUT"}, "No sequence to crossfade to")
            return {"CANCELLED"}

        if self.force_length:
            # Variables to move the second sequence
            target_frame = seq[0].frame_final_end
            frame_offset = -1 * (
                seq[1].frame_final_start - seq[0].frame_final_end)
            strip_duration = seq[1].frame_final_duration
            # Moving and trimming the second sequence
            seq[1].frame_final_start = target_frame
            seq[1].frame_final_end = target_frame + strip_duration
            sequencer.select_all(action='DESELECT')
            seq[1].select = True

            sequencer.slip(offset=frame_offset)
            seq[1].frame_final_start -= self.crossfade_length

        for s in seq:
            s.select = True

        bpy.context.scene.sequence_editor.active_strip = seq[1]
        sequencer.effect_strip_add(type='GAMMA_CROSS')
        return {"FINISHED"}


# FIXME: bug if selecting effect strips
# TODO: If single strip, use the full source so you can slide it?
# TODO: if speed already applied, update speed?
# Means need function to unspeed and redo?
class AddSpeed(bpy.types.Operator):
    bl_idname = "gdquest_vse.speed_up_sequence"
    bl_label = "Speed up Sequence"
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
    bl_idname = 'gdquest_vse.find_linked_effect'
    bl_label = 'Select linked effect'
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
    Concatenates selected strips or a channel based on the active strip
    Recommended shortcut: Shift C
    """
    bl_idname = "gdquest_vse.concatenate_strips"
    bl_label = "Concatenate strips"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sequences = []
        channels = []
        context = bpy.context

        if len(context.selected_sequences) == 1:
            sequences_in_channel = find_next_sequences(mode=SearchMode.CHANNEL,
                                                       sequences=None,
                                                       pick_sound=True)
            for s in sequences_in_channel:
                s.select = True
            context.scene.sequence_editor.active_strip.select = True

        for s in context.selected_sequences:
            if s.type in SequenceTypes.VIDEO or s.type in SequenceTypes.SOUND:
                sequences.append(s)
                channels.append(s.channel)

        if not len(sequences) >= 1:
            return {'CANCELLED'}

        from operator import attrgetter
        # sort sequences by channel and frame start
        sequences = sorted(sequences,
                           key=attrgetter('channel', 'frame_final_start'))
        channels = set(channels)
        channels = list(channels)

        for channel in channels:
            concat_start = 0
            concat_sequences = []
            for s in sequences:
                if s.channel == channel:
                    concat_sequences.append(s)
            concat_start = concat_sequences[0].frame_final_end
            concat_sequences.pop(0)

            for s in concat_sequences:
                gap = s.frame_final_start - concat_start
                s.frame_start -= gap
                concat_start += s.frame_final_duration
        return {"FINISHED"}


class SelectShortStrips(bpy.types.Operator):
    bl_idname = "gdquest_vse.select_short_strips"
    bl_label = "Select short strips"
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
    bl_idname = "gdquest_vse.smart_snap"
    bl_label = "Smart snap strip handles"
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
    bl_idname = "gdquest_vse.grab_still_image"
    bl_label = "Grab still image from active strip"
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
    bl_idname = 'gdquest_vse.toggle_sequences_muted'
    bl_label = 'Toggle sequences muted'
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
    bl_idname = 'gdquest_vse.channel_offset'
    bl_label = 'Channel offset'
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
        from operator import attrgetter
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
    bl_idname = "gdquest_vse.snap_selection_to_cursor"
    bl_label = "Snap selection to cursor"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        from operator import attrgetter
        selection = sorted(bpy.context.selected_sequences,
                           key=attrgetter('frame_final_start'))

        time_move = selection[
            0].frame_final_start - bpy.context.scene.frame_current

        from .functions.sequences import get_empty_channel
        empty_channel = get_empty_channel()

        for s in selection:
            if s.type in SequenceTypes.VIDEO or s.type in SequenceTypes.IMAGE or s.type in SequenceTypes.SOUND:
                s.frame_start -= time_move
        return {'FINISHED'}


class BorderSelect(bpy.types.Operator):
    bl_idname = 'gdquest_vse.border_select'
    bl_label = 'Border select'
    bl_description = 'Wrapper around Blender\'s border select, \
    deselects handles'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for s in bpy.context.selected_sequences:
            s.select_right_handle = False
            s.select_left_handle = False
        return bpy.ops.sequencer.select_border('INVOKE_DEFAULT', extend=False)


class GrabSequenceHandles(bpy.types.Operator):
    """
    Operator that extends the sequence based on the mouse position.
    If the cursor is to the right of the sequence's middle,
    it moves the right handle.
    If it's on the left side, it moves the left handle.
    """
    bl_idname = 'gdquest_vse.grab_sequence_handle'
    bl_label = 'Grab sequence handles'
    bl_description = 'Grabs the sequence\'s handle based on the mouse position'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        frame, _ = context.region.view2d.region_to_view(
            x=event.mouse_region_x,
            y=event.mouse_region_y)

        active = bpy.context.scene.sequence_editor.active_strip
        middle = active.frame_final_start + active.frame_final_duration / 2

        bpy.ops.sequencer.select_all(action='DESELECT')
        if frame >= middle:
            active.select_right_handle = True
        else:
            active.select_left_handle = True
        active.select = True

        bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
        return {'FINISHED'}


class PreviewLastCut(bpy.types.Operator):
    """
    Finds the closest cut to the time cursor and
    sets the preview to a small range around that frame.
    If the preview matches the range, resets to the full timeline
    """
    bl_idname = 'gdquest_vse.preview_last_cut'
    bl_label = 'Preview last cut'
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