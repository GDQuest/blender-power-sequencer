import bpy
import os
from math import ceil
from operator import attrgetter
from enum import Enum


# -----
# Global variables
# -----
class SearchMode(Enum):
    next = 1
    channel = 2
    all = 3
    pass

# -----
# Functions
# -----
# Returns the video sequence following the active one
def find_next_sequences(mode, pick_sound=False, pick_image=False):
    # some handy variables. All selected sequences, the active one, the current scene and current frame.
    selected = bpy.context.selected_sequences
    active = bpy.context.scene.sequence_editor.active_strip
    scene = bpy.context.scene
    frame = scene.frame_current
    # Stores the sequences after the selected sequence
    nexts = []
    nexts_far = []
    same_channel = []

    # Find all selected sequences to the right of the active sequence
    if selected != []:
        for s in selected:
            # current sequence is after selected sequence or is overlapping it
            if (s.frame_final_start >= active.frame_final_end) or (
                    s.frame_final_start > active.frame_final_start) & (
                        s.frame_final_start < active.frame_final_end) & (
                            s.frame_final_end > active.frame_final_end):
                # store strips in 2 lists: neighboring ones and distant ones (in terms of channels)
                if abs(s.channel - active.channel) < 2:
                    # Skip sound type in channel by default
                    if pick_sound == False and s.type == 'SOUND':
                        pass
                    elif pick_image == False and s.type == 'IMAGE':
                        pass
                    else:
                        nexts.append(s)
                        if mode == SearchMode.channel.value and s.channel == active.channel:
                            same_channel.append(s)
                else:
                    nexts_far.append(s)

    if mode == SearchMode.channel.value:
        # In channel mode, return all strips in the same channel
        return same_channel
    elif len(nexts) > 0:
        # Returns the sequence with the closest starting frame, in a neighboring channel in priority
        return min(
            nexts,
            key=
            lambda next: (next.frame_final_start - active.frame_final_start))
    # If there are no strips in neighbor channels, it fades with the closest overlapping strip
    elif len(nexts_far) > 0:
        return min(
            nexts_far,
            key=
            lambda next: (next.frame_final_start - active.frame_final_start))
    else:
        return False


def fade_create(sequences = None, fade_length = 12, fade_type = 'both'):
    """Takes a list of sequences, and adds a fade to the left, right or to both sides of the VSE strips
    fade_length: length of the fade in frames
    fade_type: 'left', 'right' or 'both' """

    scene = bpy.context.scene
    # anim_data = scene.animation_data

    # If there's no existing animation data and action in the scene, we create them.
    if scene.animation_data == None:
        scene.animation_data_create()
    if scene.animation_data.action == None:
        action = bpy.data.actions.new(scene.name + "Action")
        scene.animation_data.action = action

    fcurves = scene.animation_data.action.fcurves

    if sequences:
        # For now, clear fades and re-create the animation data
        # TODO: Smarter fades, that actually detect existing fades
        fade_clear(sequences)

        for s in sequences:
            # Setting up tuples to add keyframes for the fades later
            s_start = s.frame_final_start
            s_end = s.frame_final_end

            fade_in_frames = (s_start, s_start + fade_length)
            fade_out_frames = (s_end - fade_length, s_end)

            # TODO: Currently, the fades are always cleared, so fade_find_fcurve will always return None,
            # but it does return fade_type, which we need.
            fade_fcurve, fade_curve_type = fade_find_fcurve(s)
            # In case there's no existing fade anim, we create it
            if fade_fcurve == None:
                fade_fcurve = fcurves.new(
                    data_path=s.path_from_id(fade_curve_type))

            # Value to fade from and to - currently always 1
            # TODO: give the option to use the fade_curve's highest value?
            fade_max_value = 1

            # Sanity check - only insert keyframes if the strip is long enough
            strip_min_length = fade_length * 2 if fade_type == 'both' else fade_length

            if s.length > strip_min_length:
                # TODO: Smarter fades, that actually detect existing fades
                # Storing keyframes from the sequence's opacity/volume fcurve
                keyframes = fade_fcurve.keyframe_points
                # FADES
                if 'left' or 'both' in fade_type:
                    keyframes.insert(frame=fade_in_frames[0], value=0)
                    keyframes.insert(frame=fade_in_frames[1], value=fade_max_value)
                    if 'right' or 'both' in fade_type:
                        keyframes.insert(frame=fade_out_frames[0], value=fade_max_value)
                        keyframes.insert(frame=fade_out_frames[1], value=0)
            else:
                print('The strip ' + s.name + ' is too short for the fade to be applied.')
    return len(sequences)


def fade_find_fcurve(sequence = None):
    """Checks if there's existing fade animation on a given video sequence.
    If so, returns the data path to the corresponding fcurve.
    Also returns the strip's fade type"""

    fcurves = bpy.context.scene.animation_data.action.fcurves

    if sequence:
        if sequence.type == 'SOUND':
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


def fade_clear(sequences = None):
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


# ---------------- Operators -----------------------
# --------------------------------------------------

# TODO: Fix poll methods, use queries that make more sense.

# Auto add crossfade from the active clip to the closest next clip in the VSE
# Currently doesn't have any options
class AddCrossfade(bpy.types.Operator):
    bl_idname = "gdquest_vse.add_crossfade"
    bl_label = "Add Crossfade"
    bl_description = "Adds a Gamma Cross fade layer effect between the selected layer and the closest one to its right."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        # Find the next sequence
        first_sequence = bpy.context.scene.sequence_editor.active_strip
        bpy.ops.sequencer.select_all(action='SELECT')
        second_sequence = find_next_sequences(SearchMode.next)
        bpy.ops.sequencer.select_all(action='DESELECT')

        if (first_sequence != False) & (second_sequence != False):
            # Select only the 2 sequences required for the operation
            first_sequence.select = True
            second_sequence.select = True
            # Set second strip active so the fade goes in the right direction
            bpy.context.scene.sequence_editor.active_strip = second_sequence
            # Add crossfade
            bpy.ops.sequencer.effect_strip_add(type='GAMMA_CROSS')
        return {"FINISHED"}


# Makes it easier to speed up footage
# TODO: Add property to change how much it gets sped up
class AddSpeed(bpy.types.Operator):
    bl_idname = "gdquest_vse.add_speed"
    bl_label = "Speed up Sequence"
    bl_description = "Adds a speed effect over your clip, sets its speed and size, and wraps it into a meta strip set to over drop for easier editing"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        scene = bpy.context.scene
        active = scene.sequence_editor.active_strip

        selection = bpy.context.selected_sequences
        num_selected_strips = len(selection)

        if num_selected_strips == 0:
            active.select = True
            pass
        elif len(selection) == 1 and active.name != selection[0].name:
            active = selection[0]
            scene.sequence_editor.active_strip = active
            sequencer.refresh_all()
        # If multiple strips are selected, meta them
        elif len(selection) > 1:
            bpy.ops.sequencer.select_grouped(type='EFFECT_LINK')
            sequencer.meta_make()
            active = selection[0]
            pass

        if active.type == 'MOVIE' or active.type == 'MOVIECLIP':
            sequencer.effect_strip_add(type='SPEED')
            effect_strip = bpy.context.scene.sequence_editor.active_strip
            effect_strip.use_default_fade = False
            effect_strip.speed_factor = 2

            # Select the originally selected strip and make it active
            sequencer.select_all(action='DESELECT')
            active.select_right_handle = True
            active.select = True
            bpy.context.scene.sequence_editor.active_strip = active

            # Setting the length of the video clip to reflect the change of size
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

        # If only the active strip is selected, select all next seq in the same channel
        if len(bpy.context.selected_sequences) == 1:
            bpy.ops.sequencer.select_all(action='SELECT')
            # Select all seqs in channel, including sound and image
            sequences_in_channel = find_next_sequences(
                SearchMode.channel.value, True, True)
            bpy.ops.sequencer.select_all(action='DESELECT')
            for s in sequences_in_channel:
                s.select = True
                pass
            # We have to reselect the active strip, as find_next_sequences only returns next seqs in the channel
            bpy.context.scene.sequence_editor.active_strip.select = True
            pass
        for s in bpy.context.selected_sequences:
            if s.type == 'MOVIE' or s.type == 'SOUND' or s.type == 'META':
                sequences.append(s)
                channels.append(s.channel)
                pass
            pass

        if len(sequences) >= 1:
            # sort sequences by channel and frame start
            sequences = sorted(sequences,
                               key=attrgetter('channel', 'frame_final_start'))
            channels = set(channels)
            channels = list(channels)
            num_channels = len(channels)

            # loop over all channels to concatenate
            c = 0
            while c < num_channels:
                # The sequences are ordered, so we know that the first sequence will be the first one we'll concatenate
                concat_channel = channels[c]
                concat_start = 0
                for s in sequences:
                    if s.channel == concat_channel:
                        concat_start = s.frame_final_end
                        break
                    pass

                concat_sequences = []
                # move sequences with the channel we want to concat from the original list to the empty one
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

# TODO: (?) filter selection down only to relevant strip types (video, sound, img, meta, transform etc.)
# TODO: Smart filtering of the selection: apply fades to parent effects only
class FadeStrips(bpy.types.Operator):
    bl_idname = "gdquest_vse.fade_strips"
    bl_label = "Fade strips"
    bl_description = "Fade left, right or both sides of all selected strips in the VSE"
    bl_options = {'REGISTER', 'UNDO'}

    fade_length = bpy.props.IntProperty( name = "Fade length", description = "Length of the fade in frames", default = 12, min = 1)
    fade_type = bpy.props.StringProperty( name = "Fade type", description = "Sides of the strips to apply the fade to. 'left', 'right' or 'both'", default = 'both')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        fade_create(bpy.context.selected_sequences, self.fade_length, self.fade_type)
        return {"FINISHED"}



# TODO: add property to change the max length of selected strips
class SelectShortStrips(bpy.types.Operator):
    """Picks all the strips that are less than 8 frames long in the selection"""
    bl_idname = "gdquest_vse.select_short_strips"
    bl_label = "Select short strips"
    bl_description = "Picks all the strips that are less than 8 frames long in the selection"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        selected = bpy.context.selected_sequences
        sequencer = bpy.ops.sequencer
        strips = []

        if len(selected) > 0:
            for s in selected:
                if s.frame_final_duration < 8:
                    strips.append(s)
                    pass
                pass
            sequencer.select_all(action='DESELECT')
            for s in strips:
                s.select = True
                pass
            pass
        return {"FINISHED"}

# TODO: Ensure that strips are sorted per channel and per starting or end frame based on snap side
class SmartSnap(bpy.types.Operator):
    """Trims, extends and snaps selected strips to cursor"""
    bl_idname = "gdquest_vse.smart_snap"
    bl_label = "Trim or extend strip to cursor"
    bl_options = {'REGISTER', 'UNDO'}

    side = bpy.props.StringProperty( name = "Snap side", description = "Handle side to use to snap to, either left or right", default = 'LEFT')

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        # Extends, trims or snap every sequence based on the side we want to work with and the strip's position relative to cursor
        sequencer = bpy.ops.sequencer
        current_frame = bpy.context.scene.frame_current
        side = self.side

        for s in bpy.context.selected_sequences:
            # Deselect handles
            s.select_left_handle = False
            s.select_right_handle = False
            # Select the handle we want to snap
            if side == 'LEFT' and current_frame < s.frame_final_end:
                sequencer.select_handles(side=side)
            elif side == 'RIGHT' and current_frame > s.frame_final_start:
                sequencer.select_handles(side=side)
            else:
                s.select = False

        sequencer.snap(frame=current_frame)

        for s in context.selected_sequences:
            s.select_right_handle = False
            s.select_left_handle = False
        return {"FINISHED"}



def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)
