import bpy
from operator import attrgetter

from .utils.doc import doc_brief, doc_description, doc_idname, doc_name
from .utils.get_frame_range import get_frame_range
from .utils.get_mouse_view_coords import get_mouse_frame_and_channel
from .utils.global_settings import SequenceTypes
from .utils.slice_contiguous_sequence_list import slice_selection


class POWER_SEQUENCER_OT_ripple_delete(bpy.types.Operator):
    """
    Delete selected strips and remove remaining gaps
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'X', 'value': 'PRESS', 'shift': True}, {}, 'Ripple Delete')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.sequences

    def invoke(self, context, event):
        # Auto select if no strip selected
        frame, channel = get_mouse_frame_and_channel(context, event)
        if not context.selected_sequences:
            bpy.ops.power_sequencer.select_closest_to_mouse(frame=frame, channel=channel)
        if not context.selected_sequences:
            return {'CANCELLED'}
        return self.execute(context)

    def execute(self, context):
        scene = context.scene
        sequencer = bpy.ops.sequencer
        selection = context.selected_sequences

        audio_scrub_active = context.scene.use_audio_scrub
        context.scene.use_audio_scrub = False

        cursor_start = scene.frame_current
        cursor_offset = 0
        selection_blocks = slice_selection(context, selection)
        channels = set((s.channel for s in selection))
        is_single_channel = len(selection_blocks) == 1 and len(channels) == 1

        surrounding_strips = []
        if is_single_channel:
            bpy.ops.sequencer.select_linked()
            for s in context.selected_sequences:
                if s not in selection:
                    surrounding_strips.append(s)
            sequencer.select_all(action='DESELECT')
            for s in selection_blocks[0]:
                s.select = True
            sequencer.delete()
        else:
            for block in selection_blocks:
                sequencer.select_all(action='DESELECT')
                for s in block:
                    s.select = True
                selection_start, _ = get_frame_range(context, block)
                sequencer.delete()

                scene.frame_current = selection_start
                bpy.ops.power_sequencer.remove_gaps()

        # Concatenate if ripple delete in a single channel
        if is_single_channel:
            for s in surrounding_strips:
                s.select = True
            bpy.ops.power_sequencer.concatenate_strips()

        # scene.frame_current = cursor_start - cursor_offset
        self.report({'INFO'},
                    'Deleted ' + str(len(selection)) + ' sequence' + \
                    's' if len(selection) > 1 else '')

        context.scene.use_audio_scrub = audio_scrub_active
        return {'FINISHED'}
