import os
from enum import Enum
from math import ceil

import bpy


# -----
# GLOBAL VARIABLES
# -----
class SearchMode(Enum):
    next = 1
    channel = 2
    all = 3
    pass

sequence_types = {'video': ('MOVIE', 'MOVIECLIP', 'META', 'SCENE'),
                  'effect': ('CROSS', 'ADD', 'SUBTRACT', 'ALPHA_OVER',
                             'ALPHA_UNDER', 'GAMMA_CROSS', 'MULTIPLY',
                             'OVER_DROP', 'WIPE', 'GLOW', 'TRANSFORM', 'COLOR',
                             'SPEED', 'ADJUSTMENT', 'GAUSSIAN_BLUR'),
                  'sound': 'SOUND',
                  'image': 'IMAGE',
                  'img': 'IMAGE'}


# -----
# FUNCTIONS
# -----


def is_channel_free(target_channel, start_frame, end_frame):
    """Checks if the selected channel is empty or not. Optionally verifies that there is space in the channel in a certain timeframe"""
    # Sort sequences on screen by starting frame
    sequences = [
        s for s in bpy.context.sequences if s.channel == target_channel]

    for s in sequences:
        if start_frame <= s.frame_final_start <= end_frame or start_frame <= s.frame_final_end <= end_frame:
            return False
    return True

# to do: refactor code - clean up / get the user to pass sequences to work on?


def find_next_sequences(mode=SearchMode.next,
                        sequences=None,
                        pick_sound=False):
    """Returns a sequence or a list of sequences following the active one"""
    if sequences is None:
        sequences = bpy.context.scene.sequence_editor.sequences

    active = bpy.context.scene.sequence_editor.active_strip
    # scene = bpy.context.scene
    # frame = bpy.context.scene.frame_current
    # Stores the sequences after the selected sequence
    nexts = []
    nexts_far = []
    same_channel = []

    # Find all selected sequences to the right of the active sequence
    if sequences:
        for seq in sequences:
            # If current sequence is after selected sequence or is overlapping
            # it

            if (seq.frame_final_start >= active.frame_final_end) or (
                    seq.frame_final_start > active.frame_final_start) & (
                        seq.frame_final_start < active.frame_final_end) & (
                            seq.frame_final_end > active.frame_final_end):
                if abs(seq.channel - active.channel) > 2:
                    nexts_far.append(seq)
                else:
                    if seq.type in sequence_types['sound'] and pick_sound is False:
                        pass
                    else:
                        nexts.append(seq)
                        if mode is SearchMode.channel and seq.channel == active.channel:
                            same_channel.append(seq)

    # Store the sequences to return
    next_sequences = None
    if mode is SearchMode.channel:
        return same_channel
    elif len(nexts) > 0:
        return min(
            nexts,
            key=lambda next: (next.frame_final_start - active.frame_final_start))
    elif len(nexts_far) > 0:
        next_sequences = min(nexts_far, key=lambda next: (
            next.frame_final_start - active.frame_final_start))

    return next_sequences


# --------------
# FADE MANAGEMENT
# --------------
def fade_create(sequences=None, fade_length=12, fade_type='both'):
    """Takes a list of sequences, and adds a fade to the left, right or to both sides of
     the VSE strips.
    fade_length: length of the fade in frames
    fade_type: 'left', 'right' or 'both' """

    scene = bpy.context.scene

    if scene.animation_data is None:
        scene.animation_data_create()
    if scene.animation_data.action is None:
        action = bpy.data.actions.new(scene.name + "Action")
        scene.animation_data.action = action

    fcurves = scene.animation_data.action.fcurves

    if sequences:
        # For now, clear fades and re-create the animation data
        # to do: Smarter fades, that actually detect existing fades
        fade_clear(sequences)

        for s in sequences:
            s_start = s.frame_final_start
            s_end = s.frame_final_end

            fade_in_frames = (s_start, s_start + fade_length)
            fade_out_frames = (s_end - fade_length, s_end)

            # to do: Currently, the fades are always cleared, so fade_find_fcurve will always return None,
            # but it does return fade_type, which we need.
            fade_fcurve, fade_curve_type = fade_find_fcurve(s)
            # In case there's no existing fade anim, we create it
            if fade_fcurve is None:
                fade_fcurve = fcurves.new(
                    data_path=s.path_from_id(fade_curve_type))

            # to do: give the option to use the fade_curve's highest value?
            fade_max_value = 1

            # Sanity check - only insert keyframes if the strip is long enough
            strip_min_length = fade_length * 2 if fade_type == 'both' else fade_length

            if s.frame_final_duration > strip_min_length:
                # to do: Smarter fades, that actually detect existing fades
                keyframes = fade_fcurve.keyframe_points

                # CREATING FADE KEYFRAMES
                if fade_type in ['left', 'both']:
                    keyframes.insert(frame=fade_in_frames[0], value=0)
                    keyframes.insert(frame=fade_in_frames[1],
                                     value=fade_max_value)
                if fade_type in ['right', 'both']:
                    keyframes.insert(frame=fade_out_frames[0],
                                     value=fade_max_value)
                    keyframes.insert(frame=fade_out_frames[1], value=0)
            else:
                print('The strip ' + s.name +
                      ' is too short for the fade to be applied.')
    return len(sequences)

def fade_find_fcurve(sequence=None):
    """Checks if there's existing fade animation on a given video sequence.
    If so, returns the data path to the corresponding fcurve.
    Also returns the strip's fade type"""

    fcurves = bpy.context.scene.animation_data.action.fcurves

    if sequence:
        if sequence.type in sequence_types['sound']:
            fade_type = 'volume'
        else:
            fade_type = 'blend_alpha'

        fade_fcurve = None
        for c in fcurves:
            if (c.data_path == 'sequence_editor.sequences_all["' +
                    sequence.name + '"].' + fade_type):
                fade_fcurve = c
                break
    return fade_fcurve, fade_type


def fade_clear(sequences=None):
    """Deletes all keyframes in the blend_alpha or volume fcurves of the provided sequences"""

    fcurves = bpy.context.scene.animation_data.action.fcurves

    if sequences:
        for s in sequences:
            fade_fcurve = fade_find_fcurve(s)[0]
            if fade_fcurve:
                fcurves.remove(fade_fcurve)
        return 'Done'
    else:
        return False


def select_strip_handle(sequences, side=None, frame=None):
    """Select the left or right handles of the strips based on the frame number"""
    if not side and sequences and frame:
        return False

    side = side.upper()

    for seq in sequences:
        seq.select_left_handle = False
        seq.select_right_handle = False

        handle_side = ''

        start, end = seq.frame_final_start, seq.frame_final_end

        if side == 'AUTO' and start <= frame <= end:
            handle_side = 'LEFT' if abs(
                frame - start) < seq.frame_final_duration / 2 else 'RIGHT'
        elif side == 'LEFT' and frame < end or side == 'RIGHT' and frame > start:
            handle_side = side
        else:
            seq.select = False
        if handle_side:
            bpy.ops.sequencer.select_handles(side=handle_side)
    return True

# --------------
# CUSTOM PROPERTIES
# --------------

# to do: function to add a custom property, set it

# def add_custom_property(sequences, name, value):
#     """ Appends a new custom property to a list of sequences, and initializes it. """
#     for s in sequences:
#         bpy.ops.wm.properties_add(data_path="scene.sequence_editor")

# def remove_custom_property(sequences, name):
#     """ Removes a custom property from all selected strips, based on the property's name
#     Takes a list of sequences as input """
#     for s in sequences:
#         pass

# ---------------- Operators -----------------------
# --------------------------------------------------

# Auto add crossfade from the active clip to the closest next clip in the VSE
# Currently doesn't have any options
# DONE: Add property and option to force length of crossfade (i.e. 12 frames)
# DONE: Make it work with pictures -> add fade from and to pictures
# DONE: Refactor code - clean up
# DONE: Extend the second strip when force_length is True by crossfade_length frames
# DONE: If selected audio + video and audio is active, set video to active
# DONE: If only one audio strip selected, report error to the user
# to do: Add custom properties to the sequences referencing the GAMMA_CROSS strip, to easily remove it or process it with Python
# FIXME: Only add new crossfade if there's no existing GAMMA_CROSS between the 2 selected strips
# to do: If crossfade between effect strips or 2 pictures, set crossfade strip to ALPHA_OVER
# to do: Add custom property to store the name/data_path of the GAMMA_CROSS effect added to both strips, so we can detect it later
# to do: The operator should preserve strips with linked times (1 video + 1 audio)
# FIXME: Spotted an offset issue with a metastrip that was exactly self.crossfade_length frames before the end of the active strip
# Happens in particular if the second strip is already in place - it adds
# 10 frames at the end


class AddCrossfade(bpy.types.Operator):
    bl_idname = "gdquest_vse.add_crossfade"
    bl_label = "Add Crossfade"
    bl_description = "Adds a Gamma Cross fade layer effect between \
                      the selected layer and the closest one to its right."
    bl_options = {"REGISTER", "UNDO"}

    crossfade_length = bpy.props.IntProperty(
        name="Crossfade length",
        description="Length of the crossfade in frames",
        default=10,
        min=1)
    force_length = bpy.props.BoolProperty(
        name="Force crossfade length",
        description="When true, moves the second strip so the crossfade \
                     is of the length set in 'Crossfade Length'",
        default=True)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        active_strip = bpy.context.scene.sequence_editor.active_strip
        selection = bpy.context.selected_sequences

        # If the active strip is not a video or a meta strip, we need to run a
        # few checks

        if active_strip.type not in sequence_types['video']:
            for s in selection:
                if s.type in sequence_types['video']:
                    bpy.context.scene.sequence_editor.active_strip = s
                    active_strip = s
                    break
                pass
            # If no strip in selection is a video, can't apply crossfade
            if active_strip.type not in sequence_types['video']:
                self.report(
                    {"ERROR_INVALID_INPUT"},
                    "You need to select a video sequence to add a crossfade")
                return {"CANCELLED"}
            pass

        seq = [active_strip, find_next_sequences(SearchMode.next)]
        # Force crossfade_length
        if seq[0] and seq[1]:
            if self.force_length:
                # Setting up variables to properly relocate the second sequence
                target_frame = seq[0].frame_final_end
                frame_offset = -1 * \
                    (seq[1].frame_final_start - seq[0].frame_final_end)

                strip_duration = seq[1].frame_final_duration

                # Moving and trimming the second sequence
                seq[1].frame_final_start = target_frame
                seq[1].frame_final_end = target_frame + strip_duration
                sequencer.select_all(action='DESELECT')
                seq[1].select = True
                sequencer.slip(offset=frame_offset)
                # Moving the left handle before we apply the crossfade
                seq[1].frame_final_start -= self.crossfade_length
                pass

            # Select only the 2 sequences required for the operation
            for s in seq:
                s.select = True
            # Set second strip active so the fade goes in the right direction
            bpy.context.scene.sequence_editor.active_strip = seq[1]
            sequencer.effect_strip_add(type='GAMMA_CROSS')
        return {"FINISHED"}


# Makes it easier to speed up footage
# DONE: Add property for speed multiplier
# DONE: Fix error if selecting strip with audio
# DONE: If audio strip is active, set a video strip active instead
# DONE: Ensure that there's at least one relevant strip to speed up in the selection
# to do: if single strip selected that has a crossfade, remove it, store the source strips, run speed operator and add crossfade again
# to do: if there are multiple selected blocks of strips that are not connected in time, speed up each block separately
# to do: ? Tag the final meta strip with a custom property to know that the
# footage was sped up

class AddSpeed(bpy.types.Operator):
    bl_idname = "gdquest_vse.add_speed"
    bl_label = "Speed up Sequence"
    bl_description = "Adds a speed effect over your clip, sets its speed and size, and wraps it into a meta strip set to over drop for easier editing"
    bl_options = {"REGISTER", "UNDO"}

    speed_factor = bpy.props.IntProperty(
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

        # If the active strip is not a video strip, ensure that there are video
        # type strips in the selection and set the active strip to one of them

        if active.type not in sequence_types['video']:
            count = 0
            for s in selection:
                if s.type in sequence_types['video']:
                    scene.sequence_editor.active_strip = active = s
                    break
                else:
                    count += 1
            if count == len(selection):
                self.report(

                    {"ERROR_INVALID_INPUT"},

                    "You must select at least 1 video or meta strip to apply a speed effect - operation cancelled")

                return {"CANCELLED"}

        if len(selection) == 0:
            active.select = True
            pass
        elif len(selection) == 1 and active.name != selection[0].name:
            active = selection[0]
            scene.sequence_editor.active_strip = active
            sequencer.refresh_all()
        # Speed up with more than 1 selected strips
        elif len(selection) > 1:
            # to do: break down selection in blocks of strips that are connected
            # in time, and apply the code below to each block separately.

            def split_sequence_blocks(sequences):
                """Breaks down a selection of sequences into sub-selections of strips connected in time.
                Takes a list of sequences as input and returns a tuple of lists. Each returned list represents a block of sequences that are connected in time.
                Use this function to apply an operator that works with blocks of sequences, like gdquest_vse.add_speed"""

                # Sort sequences by start time
                # Step through the sequences and mark the ones between which there's a gap with a breakpoint (cut index)
                # Loop through the breakpoints to split the lists to return
                pass

            bpy.ops.sequencer.select_grouped(type='EFFECT_LINK')
            # If there are no effect strips with the selection, Blender will deselect everything. Then we have to use the original selection
            # to do: Check if it works if there are effects only on some of the
            # selected strips?

            for s in selection:
                if not s in bpy.context.selected_sequences:
                    s.select = True
            sequencer.meta_make()
            active = scene.sequence_editor.active_strip
            pass

        if active.type in sequence_types['video']:
            sequencer.effect_strip_add(type='SPEED')
            effect_strip = bpy.context.scene.sequence_editor.active_strip
            effect_strip.use_default_fade = False
            effect_strip.speed_factor = self.speed_factor

            # Select the originally selected strip and make it active
            sequencer.select_all(action='DESELECT')
            active.select_right_handle = True
            active.select = True
            bpy.context.scene.sequence_editor.active_strip = active

            # Setting the length of the video clip to reflect the change of
            # size

            size = ceil(active.frame_final_duration /
                        effect_strip.speed_factor)
            endFrame = active.frame_final_start + size
            sequencer.snap(frame=endFrame)

            effect_strip.select = True
            sequencer.meta_make()
            pass
            pass
        return {"FINISHED"}

# Shortcut: Shift + C
# to do: If only one selected strip per channel, concatenate all channels
# individually


class ConcatenateStrips(bpy.types.Operator):
    """Concatenates selected strips or a channel based on the active strip"""
    bl_idname = "gdquest_vse.concatenate_strips"
    bl_label = "Concatenate strips"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        sequences = []
        channels = []

        # If only the active strip is selected, select all next seq in the same
        # channel

        if len(bpy.context.selected_sequences) == 1:
            # Select all seqs in channel, including sound and image
            sequences_in_channel = find_next_sequences(mode=SearchMode.channel,
                                                       sequences=None,
                                                       pick_sound=True,
                                                       pick_image=True)
            for s in sequences_in_channel:
                s.select = True
            # We have to reselect the active strip, as find_next_sequences only
            # returns next seqs in the channel

            bpy.context.scene.sequence_editor.active_strip.select = True
        for s in bpy.context.selected_sequences:
            if s.type in sequence_types['video']:
                sequences.append(s)
                channels.append(s.channel)
                pass
            pass

        if len(sequences) >= 1:
            from operator import attrgetter

            # sort sequences by channel and frame start
            sequences = sorted(sequences,
                               key=attrgetter('channel', 'frame_final_start'))
            channels = set(channels)
            channels = list(channels)
            num_channels = len(channels)

            # to do: If the number of channels the sequences are spread other is equal to the number of selected sequences, then there's only 1 selected sequence per channel
            # So then we select all next sequences in each channel
            # Gotta refactor the find_next_sequences so we have to pass it a channel if mode == SearchMode.channel
            # if num_channels == len(sequences):
            #     for c in channels:
            #         for s in find_next_sequences(mode=SearchMode.channel,
            #                                                    sequences=None,
            #                                                    pick_sound=True,
            #                                                    pick_image=True)
            # loop over all channels to concatenate
            c = 0
            while c < num_channels:
                # The sequences are ordered, so we know that the first sequence
                # will be the first one we'll concatenate

                concat_channel = channels[c]
                concat_start = 0
                for s in sequences:
                    if s.channel == concat_channel:
                        concat_start = s.frame_final_end
                        break
                    pass

                concat_sequences = []
                # move sequences with the channel we want to concat from the
                # original list to the empty one

                for s in sequences:
                    if s.channel == concat_channel:
                        concat_sequences.append(s)
                        pass
                    pass
                concat_sequences.pop(0)
                for s in concat_sequences:
                    gap = s.frame_final_start - concat_start
                    s.frame_start -= gap
                    concat_start += s.frame_final_duration
                    pass
                pass
                c += 1
            pass
        return {"FINISHED"}


# to do: (?) filter selection down only to relevant strip types (video, sound, img, meta, transform etc.)
# to do: Smart filtering of the selection: apply fades to parent effects
# only if possible

class FadeStrips(bpy.types.Operator):
    bl_idname = "gdquest_vse.fade_strips"
    bl_label = "Fade strips"
    bl_description = "Fade left, right or both sides of all selected strips in the VSE"
    bl_options = {'REGISTER', 'UNDO'}

    fade_length = bpy.props.IntProperty(
        name="Fade length",
        description="Length of the fade in frames",
        default=12,
        min=1)
    fade_type = bpy.props.EnumProperty(
        items= [('both', 'Fade in and out', 'Fade selected strips in and out'),
                ('left', 'Fade in', 'Fade in selected strips'),
                ('right', 'Fade out', 'Fade out selected strips')],
        name="Fade type",
        description="Fade in, out, or both in and out. Default is both.",
        default='both')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # to do: Use selection or active strip otherwise
        selected_sequences = bpy.context.selected_sequences if len(
            bpy.context.
            selected_sequences) > 0 else bpy.context.scene.sequence_editor.active_strip
        fade_create(selected_sequences, self.fade_length, self.fade_type)
        return {"FINISHED"}


# DONE: add property to change the max length of selected strips
class SelectShortStrips(bpy.types.Operator):
    bl_idname = "gdquest_vse.select_short_strips"
    bl_label = "Select short strips"
    bl_description = "Filters the current selection down to the strips that are less than the 'Max strip length' frames long."
    bl_options = {'REGISTER', 'UNDO'}

    max_strip_length = bpy.props.IntProperty(
        name="Max strip length",
        description="Length of the selected strips in frames",
        default=8,
        min=1)

    @classmethod
    def poll(cls, context):
        return context.scene is not None

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

    side = bpy.props.EnumProperty(
        items=[('left', 'Left', 'Left side'),
               ('right', 'Right', 'Right side'),
               ('auto', 'Auto', 'Use the side closest to the time cursor')],
        name="Snap side",
        description="Handle side to use for the snap",
        default='auto')

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        current_frame = bpy.context.scene.frame_current

        select_strip_handle(
            bpy.context.selected_sequences, self.side, current_frame)

        sequencer.snap(frame=current_frame)

        for s in context.selected_sequences:
            s.select_right_handle = False
            s.select_left_handle = False
        return {"FINISHED"}

# to do: Ripple strips on the first transform
class GrabStillImage(bpy.types.Operator):
    """Grabs a still image from the active video strip, to quickly achieve pause effects"""
    bl_idname = "gdquest_vse.grab_still_image"
    bl_label = "Grab still image from active strip"
    bl_options = {'REGISTER', 'UNDO'}

    strip_duration = bpy.props.IntProperty(
        name="Strip duration",
        description="Duration of the still image strip in frames",
        default=106)

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        scene = bpy.context.scene
        active = scene.sequence_editor.active_strip
        sequencer = bpy.ops.sequencer
        transform = bpy.ops.transform

        start_frame = scene.frame_current
        offset = self.strip_duration

        if active.type not in sequence_types['video']:
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
        sequencer.cut(frame=scene.frame_current, type='SOFT', side='RIGHT')
        transform.seq_slide(value=(offset, 0))
        sequencer.cut(frame=scene.frame_current + offset + 1, type='SOFT', side='LEFT')
        transform.seq_slide(value=(-offset, 0))

        sequencer.meta_make()
        active = scene.sequence_editor.active_strip
        active.name = 'Still image'
        active.select_right_handle = True
        transform.seq_slide(value=(offset, 0))

        scene.frame_current = start_frame

        active.select = True
        active.select_right_handle = False
        active.select_left_handle = False
        return {"FINISHED"}


# to do: Extract function
# to do: Basic functionality, move a strip to the neighboring channel if
# it's empty, otherwise skip channels if possible
class ChannelOffset(bpy.types.Operator):
    """Moves selected strips up and down smartly. Can swap sequences or detect if a channel is not empty"""
    bl_idname = "gdquest_vse.channel_offset"
    bl_label = "Move sequences to other channels"
    bl_options = {'REGISTER', 'UNDO'}

    offset_upwards = bpy.props.BoolProperty(
        name="Offset upwards",
        description="If True, the strips will move up. Else, they will move down.",
        default=True)

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        # Sort selected layers by channel, starting from highest value if going
        # up

        from operator import attrgetter
        selected = sorted(bpy.context.selected_sequences, key=attrgetter(
            'channel'), reverse=self.offset_upwards)

        # to do: Check and move channels in selection recursively, one by one
        target_channel = selected[0].channel
        target_channel = target_channel + 1 if self.offset_upwards else target_channel - 1

        selection_start = min(selected, key=attrgetter('frame_final_start'))
        selection_end = max(selected, key=attrgetter('frame_final_end'))

        if is_channel_free(target_channel, start_frame=selection_start, end_frame=selection_end) and target_channel >= 1:
            for s in selected:
                if self.offset_upwards:
                    s.channel += 1
                elif s.channel > 1:
                    s.channel -= 1

        return {"FINISHED"}


# class AddSimpleText(bpy.types.Operator):
#     """Adds a text strip and sets it up to quickly add an animated note on the video"""
#     bl_idname = "gdquest_vse.add_simple_text"
#     bl_label = "Add a text strip and set it up quickly"
#     bl_options = {'REGISTER', 'UNDO'}

#     strip_duration = bpy.props.IntProperty(
#         name="Duration",
#         description="Length of the text strip in frames"
#         default=96
#     )
#     text = bpy.props.StringProperty(
#         name="Text",
#         description="The text to display on screen"
#         default="Text"
#     )
#     align_x = bpy.props.EnumProperty(
#         items= [('left', 'left', 'Align to the left edge of the screen'),
#                 ('middle', 'middle', 'Align to the middle of the screen'),
#                 ('right', 'right', 'Align to the right edge of the screen')],
#         name="Horizontal align",
#         description="",
#         default='right'
#     )
#     align_y = bpy.props.EnumProperty(
#         items= [('top', 'top', 'Align to the top edge of the screen'),
#                 ('middle', 'middle', 'Align to the middle of the screen'),
#                 ('bottom', 'bottom', 'Align to the bottom edge of the screen')],
#         name="Vertical align",
#         description="",
#         default='right'
#     )
#     animate = bpy.props.BoolProperty(
#         name="Animate opacity",
#         description="",
#         default=True
#     )

#     @classmethod
#     def poll(cls, context):
#         return context.scene is not None

#     def execute(self, context):
#         sequencer = bpy.ops.sequencer
#         current_frame = bpy.context.scene.frame_current

#         sequencer.effect_strip_add(
#             type='TEXT', frame_end=current_frame + self.strip_duration, replace_sel=True)
        
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

def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
