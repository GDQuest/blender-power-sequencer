import bpy


class Unspeed(bpy.types.Operator):
    """
    This is the opposite of power_sequencer's "Add Speed" operator.
    It seeks out and removes the speed modifier inside a meta and
    ungroups all the remaining strips within.
    """
    bl_idname = "power_sequencer.unspeed"
    bl_label = "Remove Speed"
    bl_description = "Removes speed from META, un-groups META"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if not (scene.sequence_editor and active_strip):
            return False
        result = active_strip.select and active_strip.type == 'META'
        result = result and [s for s in active_strip.sequences if s.type == 'SPEED']
        return result

    def execute(self, context):
        active = context.scene.sequence_editor.active_strip
        sub_strips = []
        for s in active.sequences:
            if s.type == "SPEED":
                speed_strip = s
            else:
                sub_strips.append(s)

        bpy.ops.sequencer.meta_separate()
        bpy.ops.sequencer.select_all(action='DESELECT')

        speed_strip.select = True
        bpy.ops.sequencer.delete()

        for s in sub_strips:
            s.select = True
        return {'FINISHED'}
