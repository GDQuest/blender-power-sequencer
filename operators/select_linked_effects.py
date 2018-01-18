import bpy
from .utils.find_linked_sequences import find_linked


class SelectLinkedEffect(bpy.types.Operator):
    bl_idname = 'power_sequencer.find_linked_effect'
    bl_label = 'PS.Select linked effect'
    bl_description = 'Select all strips that are linked by an effect strip'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for s in find_linked(bpy.context.selected_sequences):
            s.select = True
        return {'FINISHED'}
