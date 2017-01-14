import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty, EnumProperty

from .functions.global_settings import SequenceTypes, SearchMode
from .functions.sequences import is_channel_free, find_next_sequences, \
    select_strip_handle


# ---------------- Operators -----------------------
# --------------------------------------------------
# TODO: Rewrite cleanly
# FIXME: Make sure the offset preserves the starting frame of the second strip
# TODO: make it work with pictures and transform strips
# TODO: If source strip has a special blending mode, use that for crossfade
# TODO: If 2 strips selected and same type familly (visual or sound), crossfade
# from the bottom left one to the top right one
# TODO: Chain crossfades if more than 2 strips selected?
# TODO: Add custom properties to the sequences referencing the GAMMA_CROSS
# strip, to easily remove it or process it with Python
# FIXME: Only add new crossfade if there's no existing GAMMA_CROSS between 2
# selected strips
# TODO: If crossfade between effect strips or 2 pictures, set crossfade strip
# ALPHA_OVER
# TODO: Add custom property to store the name/data_path of the GAMMA_CROSS
# effect added to both strips, so we can detect it later
# TODO: The operator should preserve strips with linked times (1 video + 1
# audio)
# FIXME: Spotted an offset issue with a metastrip that was exactly
# self.crossfade_length frames before the end of the active strip
# Happens in particular if the second strip is already in place - it adds 10
# frames at the end
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
                     is of the length set in 'Crossfade Length'",
        default=True)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        active = bpy.context.scene.sequence_editor.active_strip
        selection = bpy.context.selected_sequences

        if len(selection) > 1:
            self.report({"ERROR_INVALID_INPUT"}, "Only select one strip to \
            crossfade from")
            return {"CANCELLED"}

        if active.type not in SequenceTypes.VIDEO:
            if selection[0].type in SequenceTypes.VIDEO:
                bpy.context.scene.sequence_editor.active_strip = active = selection[0]
            else:
                self.report({"ERROR_INVALID_INPUT"}, "You need to select a video \
                sequence to add a crossfade")
                return {"CANCELLED"}

        seq = [active, find_next_sequences(SearchMode.NEXT)]
        if not seq[0] and seq[1]:
            return {"CANCELLED"}

        if self.force_length:
            # Variables to move the second sequence
            target_frame = seq[0].frame_final_end
            frame_offset = -1 * (seq[1].frame_final_start - seq[0].frame_final_end)
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


# TODO: if single strip selected that has a crossfade, remove it, store the
# source strips, run speed operator and add crossfade again
# TODO: if there are multiple selected blocks of strips that are not connected
# in time, speed up each block separately
# TODO: ? Tag the final meta strip with a custom property to know that the
# footage was sped up, so it can be modified later
class AddSpeed(bpy.types.Operator):
    bl_idname = "gdquest_vse.add_speed"
    bl_label = "Speed up Sequence"
    bl_description = "Adds a speed effect over your clip, sets its speed and size, and wraps it into a meta strip set to over drop for easier editing"
    bl_options = {"REGISTER", "UNDO"}

    speed_factor = IntProperty(
        name="Speed factor",
        description="How many times the footage gets sped up",
        default=2,
        min=0)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        scene = bpy.context.scene
        active = scene.sequence_editor.active_strip

        selection = bpy.context.selected_sequences

        if not selection:
            self.report({"ERROR_INVALID_INPUT"}, "No sequences selected. Operation cancelled")
            return {"CANCELLED"}

        if active.type not in SequenceTypes.VIDEO:
            count = 0
            for s in selection:
                if s.type in SequenceTypes.VIDEO:
                    scene.sequence_editor.active_strip = active = s
                    break
                else:
                    count += 1
            if count == len(selection):
                self.report({"ERROR_INVALID_INPUT"}, "You must select at least 1 video or meta strip to apply a speed effect. Operation cancelled")
                return {"CANCELLED"}

        # TODO: refactor to make it work without active sequence
        # from .functions.sequences import slice_selection
        # selection_blocks = slice_selection(selection)

        # for sel in selection_blocks:
        #     sequencer.select_all(action='DESELECT')
        #     for s in sel:
        #         s.select = True

        if len(selection) == 1 and active.name != selection[0].name:
            active = scene.sequence_editor.active_strip = selection[0]
            # sequencer.refresh_all()
        elif len(selection) > 1:
            sequencer.select_grouped(type='EFFECT_LINK')
            for s in selection:
                s.select = True
            sequencer.meta_make()
            active = scene.sequence_editor.active_strip

        sequencer.effect_strip_add(type='SPEED')
        effect_strip = bpy.context.scene.sequence_editor.active_strip
        effect_strip.use_default_fade = False
        effect_strip.speed_factor = self.speed_factor

        sequencer.select_all(action='DESELECT')
        active.select_right_handle = True
        active.select = True
        scene.sequence_editor.active_strip = active

        from math import ceil
        size = ceil(active.frame_final_duration /
                    effect_strip.speed_factor)
        endFrame = active.frame_final_start + size
        sequencer.snap(frame=endFrame)

        effect_strip.select = True
        sequencer.meta_make()
        bpy.context.selected_sequences[0].name = 'Speed ' + str(self.speed_factor) + 'x'
        return {"FINISHED"}


# Shortcut: Shift + C
# TODO: If only one selected strip per channel, concatenate all channels
# individually
class ConcatenateStrips(bpy.types.Operator):
    """Concatenates selected strips or a channel based on the active strip"""
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
        sequences = sorted(sequences, key=attrgetter('channel', 'frame_final_start'))
        channels = set(channels)
        channels = list(channels)

        # TODO: If the number of channels the sequences are spread over is equal to the number of selected sequences, then there's only 1 selected sequence per channel
        # So then we select all next sequences in each channel
        # Gotta refactor the find_next_sequences so we have to pass it a channel if mode == SearchMode.CHANNEL
        # if num_channels == len(sequences):
        #     for c in channels:
        #         for s in find_next_sequences(mode=SearchMode.CHANNEL,
        #                                                    sequences=None,
        #                                                    pick_sound=True,
        #                                                    pick_image=True)
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


# DONE: add property to change the max length of selected strips
class SelectShortStrips(bpy.types.Operator):
    bl_idname = "gdquest_vse.select_short_strips"
    bl_label = "Select short strips"
    bl_description = "Filters the current selection down to the strips that are less than the 'Max strip length' frames long."
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
    bl_label = "Trim or extend strip to cursor"
    bl_options = {'REGISTER', 'UNDO'}

    side = EnumProperty(
        items=[('left', 'Left', 'Left side'),
               ('right', 'Right', 'Right side'),
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

        select_strip_handle(bpy.context.selected_sequences, self.side, current_frame)

        sequencer.snap(frame=current_frame)

        for s in context.selected_sequences:
            s.select_right_handle = False
            s.select_left_handle = False
        return {"FINISHED"}


# TODO: Ripple strips on the first transform
class GrabStillImage(bpy.types.Operator):
    """Grabs a still image from the active video strip, to quickly achieve pause effects"""
    bl_idname = "gdquest_vse.grab_still_image"
    bl_label = "Grab still image from active strip"
    bl_options = {'REGISTER', 'UNDO'}

    strip_duration = IntProperty(
        name="Strip duration",
        description="Duration of the still image strip in frames",
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
            self.report({"ERROR_INVALID_INPUT"},
                        "You must select a video or meta strip. You selected a strip of type"
                        + str(active.type) + " instead.")
            return {"CANCELLED"}
        if not active.frame_final_start <= start_frame < active.frame_final_end:
            self.report({"ERROR_INVALID_INPUT"},
                        "Your time cursor must be on the frame you want \
                        to convert to a still image.")
            return {"CANCELLED"}
        if start_frame == active.frame_final_start:
            scene.frame_current = start_frame + 1

        active.select = True
        source_blend_type = active.blend_type
        sequencer.cut(frame=scene.frame_current, type='SOFT', side='RIGHT')
        transform.seq_slide(value=(offset, 0))
        sequencer.cut(frame=scene.frame_current +
                      offset + 1, type='SOFT', side='LEFT')
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
    bl_idname = 'gdquest_vse.toggle_muted'
    bl_label = 'Toggle sequences mute'
    bl_description = 'Mute or unmute sequences'
    bl_options = {'REGISTER', 'UNDO'}

    use_unselected = BoolProperty(
        name="Use unselected",
        description="Toggle non selected sequences",
        default=False)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = bpy.context.selected_sequences

        if self.use_unselected:
            selection = [s for s in bpy.context.sequences if s not in selection]

        if not selection:
            self.report({"WARNING"}, "No sequences to toggle muted")
            return {'CANCELLED'}

        mute = not selection[0].mute
        for s in selection:
            s.mute = mute
        return {'FINISHED'}


# TODO: make it work going up
class ChannelOffset(bpy.types.Operator):
    bl_idname = 'gdquest_vse.channel_offset'
    bl_label = 'Channel offset'
    bl_description = 'Move selected strips up or down a channel'
    bl_options = {'REGISTER', 'UNDO'}

    direction = EnumProperty(items=[
        ('up', 'up', 'Move the selection 1 channel up'),
        ('down', 'down', 'Move the selection 1 channel down')],
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

        selection = sorted(selection, key=attrgetter('channel', 'frame_final_start'))

        if self.direction == 'up':
            for s in reversed(selection):
                s.channel += 1
        elif self.direction == 'down':
            for s in selection:
                if (s.channel > 1):
                    s.channel -= 1
        return {'FINISHED'}


# TODO: find a way to get the selection bounding box and place it where there is space for it.
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
        selection = sorted(bpy.context.selected_sequences, key=attrgetter('frame_final_start'))

        time_move = selection[0].frame_final_start - bpy.context.scene.frame_current

        from .functions.sequences import find_empty_channel
        empty_channel = find_empty_channel()

        for s in selection:
            channel = s.channel
            if s.type in SequenceTypes.VIDEO or s.type in SequenceTypes.IMAGE or s.type in SequenceTypes.SOUND:
                s.frame_start -= time_move
            s.channel = empty_channel + channel - 1
        return {'FINISHED'}



# TODO: Make it work
# TODO: Access font folders
# TODO: allow to define favorite fonts in add-on prefs
# class AddSimpleText(bpy.types.Operator):
#     """Adds a text strip and sets it up to quickly add an animated note on the video"""
#     bl_idname = "gdquest_vse.add_simple_text"
#     bl_label = "Add a text strip and set it up quickly"
#     bl_options = {'REGISTER', 'UNDO'}

#     strip_duration = IntProperty(
#         name="Duration",
#         description="Length of the text strip in frames"
#         default=96
#     )
#     text = StringProperty(
#         name="Text",
#         description="The text to display on screen"
#         default="Text"
#     )
#     align_x = EnumProperty(
#         items= [('left', 'left', 'Align to the left edge of the screen'),
#                 ('middle', 'middle', 'Align to the middle of the screen'),
#                 ('right', 'right', 'Align to the right edge of the screen')],
#         name="Horizontal align",
#         description="",
#         default='right'
#     )
#     align_y = EnumProperty(
#         items= [('top', 'top', 'Align to the top edge of the screen'),
#                 ('middle', 'middle', 'Align to the middle of the screen'),
#                 ('bottom', 'bottom', 'Align to the bottom edge of the screen')],
#         name="Vertical align",
#         description="",
#         default='right'
#     )
#     animate = BoolProperty(
#         name="Animate opacity",
#         description="",
#         default=True
#     )

#     @classmethod
#     def poll(cls, context):
#         return True

#     def execute(self, context):
#         sequencer = bpy.ops.sequencer
#         current_frame = bpy.context.scene.frame_current

#         sequencer.effect_strip_add(
# type='TEXT', frame_end=current_frame + self.strip_duration,
# replace_sel=True)

#         text_strip = bpy.context.selected_sequences[0]

#         init_text(text_strip, self.text, self.align_x, self.align_y, self.animate)

#         def init_text(sequence, text, align_x, align_y, animate):
#             sequence.name, sequence.text = text

#             sequence.location = (0.0, 0.0)

#             # FONT
#             # ADD TRANSFORM
#             # ADD FADE
#             if animate:
#                 pass

#             return True

#         return {"FINISHED"}
