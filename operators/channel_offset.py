import bpy
from operator import attrgetter


class ChannelOffset(bpy.types.Operator):
    bl_idname = 'power_sequencer.channel_offset'
    bl_label = 'Channel Offset'
    bl_description = 'Move selected strips up or down a channel'
    bl_options = {'REGISTER', 'UNDO'}

    direction = bpy.props.EnumProperty(
        items=[('up', 'up', 'Move the selection 1 channel up'),
               ('down', 'down', 'Move the selection 1 channel down')],
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

        selection = sorted(
            selection, key=attrgetter('channel', 'frame_final_start'))

        if self.direction == 'up':
            for s in reversed(selection):
                s.channel += 1
        elif self.direction == 'down':
            for s in selection:
                if (s.channel > 1):
                    s.channel -= 1
        return {'FINISHED'}
