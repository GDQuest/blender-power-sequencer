import bpy
import bgl
import blf
from math import floor


# Shortcut: Ctrl Click
# to do: give the ability to trim instead of cutting
# to do: allow the user to set the selection mode in the preferences
class MouseCut(bpy.types.Operator):
    """Cuts the strip sitting under the mouse"""
    bl_idname = "gdquest_vse.mouse_cut"
    bl_label = "Cut strip with mouse"
    bl_options = {'REGISTER', 'UNDO'}

    select_mode = bpy.props.EnumProperty(
        items=[('mouse', 'Mouse', 'Only select the strip hovered by the mouse'),
               ('cursor', 'Time cursor', 'Select all of the strips the time cursor overlaps')],
        name="Selection mode",
        description="Cut only the strip under the mouse or all strips under the time cursor",
        default='mouse')
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

        frame, channel = context.region.view2d.region_to_view(
            x=event.mouse_region_x,
            y=event.mouse_region_y)
        frame = floor(frame)
        channel = floor(channel)

        bpy.ops.anim.change_frame(frame=frame)

        sequencer.select_all(action='DESELECT')
        sequences_to_select = mouse_select_sequences(frame, channel, self.select_mode)
        for seq in sequences_to_select:
            seq.select = True
        
        if self.cut_mode == 'cut':
            sequencer.cut(frame=bpy.context.scene.frame_current,
                        type='SOFT',
                        side='BOTH')
        else:
            bpy.ops.gdquest_vse.smart_snap()
        return {"FINISHED"}

def mouse_select_sequences(frame=None, channel=None, mode='mouse'):
    """Selects sequences based on the mouse position or using the time cursor"""

    selection = []

    print("frame: " + str(frame))
    print("channel: " + str(channel))

    sequences = bpy.context.sequences
    if not sequences:
        return []

    for seq in bpy.context.sequences:
        if seq.channel == channel and seq.frame_final_start <= frame <= seq.frame_final_end:
            selection.append(seq)
            if mode == 'mouse':
                break
    return selection
