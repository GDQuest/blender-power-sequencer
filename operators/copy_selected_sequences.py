import bpy
from operator import attrgetter


class CopySelectedSequences(bpy.types.Operator):

    """
    ![Demo](https://i.imgur.com/w6z1Jb1.gif)

    Copies the selected sequences without frame offset and optionally
    deletes the selection to give a cut to clipboard effect. This
    operator overrides the default Blender copy method which includes
    cursor offset when pasting, which is atypical of copy/paste methods.
    """
    bl_idname = "power_sequencer.copy_selected_sequences"
    bl_label = "Copy Selected Sequences"
    bl_description = "Copy/cut strips without offset from current time indicator"
    bl_options = {'REGISTER', 'UNDO'}

    delete_selection = bpy.props.BoolProperty(
        name="Delete selection",
        description="Delete selected strips: acts like cut and paste",
        default=False)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = bpy.context.selected_sequences
        cursor_start_frame = bpy.context.scene.frame_current
        sequencer = bpy.ops.sequencer

        # Deactivate audio playback
        scene = bpy.context.scene
        initial_audio_setting = scene.use_audio_scrub
        scene.use_audio_scrub = False

        first_sequence = min(selection, key=attrgetter('frame_final_start'))
        bpy.context.scene.frame_current = first_sequence.frame_final_start
        sequencer.copy()
        bpy.context.scene.frame_current = cursor_start_frame

        scene.use_audio_scrub = initial_audio_setting

        if self.delete_selection:
            sequencer.delete()

        plural_string = 's' if len(selection) != 1 else ''
        action_verb = 'Cut' if self.delete_selection else 'Copied'
        report_message = '{!s} {!s} sequence{!s} to the clipboard.'.format(
            action_verb, str(len(selection)), plural_string)
        self.report({'INFO'}, report_message)
        return {"FINISHED"}
