import bpy


class Unspeed(bpy.types.Operator):
    """
    This is the opposite of power_sequencer's "Add Speed" operator.
    It seeks out and removes the speed modifier inside a meta and
    ungroups all the remaining strips within.
    """
    bl_idname = "power_sequencer.unspeed"
    bl_label = "Unspeed"
    bl_description = "Removes speed from META, un-groups META"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if scene.sequence_editor and scene.sequence_editor.active_strip:
            active = scene.sequence_editor.active_strip
            if active.select and active.type == "META":
                for strip in active.sequences:
                    if strip.type == "SPEED":
                        return True
        return False

    def execute(self, context):
        scene = context.scene

        active = scene.sequence_editor.active_strip

        start = active.frame_start
        end = active.frame_final_end
        duration = active.frame_duration

        print(start, end, duration)

        sub_strips = []
        for strip in active.sequences:
            if strip.type == "SPEED":
                speed_strip = strip
                speed_factor = strip.speed_factor
            else:
                sub_strips.append(strip)

        bpy.ops.sequencer.meta_separate()

        bpy.ops.sequencer.select_all(action='DESELECT')

        speed_strip.select = True
        bpy.ops.sequencer.delete()

        for strip in sub_strips:
            strip.select = True
            strip.frame_final_end = start + (duration * speed_factor) - 1

        return {'FINISHED'}



