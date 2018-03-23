import bpy
from .utils.global_settings import SequenceTypes
from operator import attrgetter


class EditCrossfade(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/rCmLhg6.gif)
    
    Selects the handles of both inputs of a crossfade strip's input and 
    calls the grab operator. Allows you to quickly change the location
    of a fade transition between two strips.
    """
    bl_idname = "power_sequencer.edit_crossfade"
    bl_label = "Edit Crossfade"
    bl_description = "Adjust the location of the crossfade between 2 strips"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.area.type == 'SEQUENCE_EDITOR':
            self.report({
                'WARNING'
            }, "You need to be in the Video Sequence Editor to use this tool. \
                        Operation cancelled.")
            return {'CANCELLED'}

        active = bpy.context.scene.sequence_editor.active_strip

        if active.type != "GAMMA_CROSS":
            effect = self.find_effect_strips(active)
            if effect is None:
                self.report({
                    'WARNING'
                }, "The active strip has to be a gamma cross for this tool to work. \
                            Operation cancelled.")
                return {"CANCELLED"}
            active = bpy.context.scene.sequence_editor.active_strip = effect[0]

        bpy.ops.sequencer.select_all(action='DESELECT')
        active.select = True
        active.input_1.select_right_handle = True
        active.input_2.select_left_handle = True
        active.input_1.select = True
        active.input_2.select = True

        bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
        return {'FINISHED'}

    def find_effect_strips(self, sequence):
        """
        Takes a single strip and finds effect strips that use it as input
        Returns the effect strip(s) found as a list, ordered by starting frame
        Returns None if no effect was found
        """
        if sequence.type not in SequenceTypes.VIDEO and sequence.type not in SequenceTypes.IMAGE:
            return None

        effect_sequences = (s
                            for s in bpy.context.sequences
                            if s.type in SequenceTypes.EFFECT)
        found_effect_strips = []
        for s in effect_sequences:
            if s.input_1.name == sequence.name:
                found_effect_strips.append(s)
            if s.input_count == 2:
                if s.input_2.name == sequence.name:
                    found_effect_strips.append(s)

        found_effect_strips = sorted(found_effect_strips,
                                     key=attrgetter('frame_final_start'))
        return found_effect_strips
