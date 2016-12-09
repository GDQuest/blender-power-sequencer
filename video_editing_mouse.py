"""Video editing tools for Blender using the mouse"""
from math import floor

import bpy


#to do: idea - handler to optionnally ripple edit automatically? And/or auto remove gaps on delete?

# Shortcut: Ctrl Click
# to do: allow the user to set the selection mode in the preferences
# to do: add option to auto remove space between strips on trim
# to do: smart mode - if not clicking on a specific strip with the mouse, use cursor mode
# to do: check how it works with effect strips? Blender should handle that by itself
class MouseCut(bpy.types.Operator):
    """Cuts the strip sitting under the mouse"""
    bl_idname = "gdquest_vse.mouse_cut"
    bl_label = "Cut strip with mouse"
    bl_options = {'REGISTER', 'UNDO'}

    select_mode = bpy.props.EnumProperty(
        items=[('mouse', 'Mouse', 'Only select the strip hovered by the mouse'),
               ('cursor', 'Time cursor', 'Select all of the strips the time cursor overlaps'),
               ('smart', 'Smart', 'Uses the selection if possible, else uses the other modes')],
        name="Selection mode",
        description="Cut only the strip under the mouse or all strips under the time cursor",
        default='smart')
    cut_mode = bpy.props.EnumProperty(
        items=[('cut', 'Cut', 'Cut the strips'),
               ('trim', 'Trim', 'Trim the selection')],
        name='Cut mode',
        description='Cut or trim the selection',
        default='cut')

    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

    def invoke(self, context, event):
        sequencer = bpy.ops.sequencer
        selection = bpy.context.selected_sequences

        frame, channel = context.region.view2d.region_to_view(
            x=event.mouse_region_x,
            y=event.mouse_region_y)
        frame = floor(frame)
        channel = floor(channel)

        bpy.ops.anim.change_frame(frame=frame)

        if self.select_mode == 'cursor':
            sequencer.select_all(action='SELECT')
        elif self.select_mode != 'smart' or len(selection) == 0:
            sequencer.select_all(action='DESELECT')
            sequences_to_select = mouse_select_sequences(frame, channel, self.select_mode)
            if not sequences_to_select:
                return {"CANCELLED"}
            for seq in sequences_to_select:
                seq.select = True
        
        if self.cut_mode == 'cut':
            sequencer.cut(frame=bpy.context.scene.frame_current,
                          type='SOFT',
                          side='BOTH')
        else:
            bpy.ops.gdquest_vse.smart_snap(side='auto')
        return {"FINISHED"}

def find_sequence_trim_side(sequence=None, frame=None):
    """Returns the strip's handle the time cursor is closest to"""
    if not sequence and frame:
        return None

    if frame >= sequence.frame_final_duration / 2:
        return 'right'
    else:
        return 'left'

def mouse_select_sequences(frame=None, channel=None, mode='mouse', select_linked=True):

    """Selects sequences based on the mouse position or using the time cursor"""

    selection = []
    sequences = bpy.context.sequences

    if not sequences:
        return []

    for seq in sequences:
        channel_check = True if seq.channel == channel else False
        if channel_check or mode == 'cursor' \
        and seq.frame_final_start <= frame <= seq.frame_final_end:
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
