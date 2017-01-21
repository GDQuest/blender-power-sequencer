"""A module to create and synchronize titles for videos,
using timeline markers, and either Image strips or Text strips"""
import bpy


# TODO: operator to synchronize pictures to markers
# Use the CreateText operator to add text strips
class SyncTitles(bpy.types.Operator):
    bl_idname = 'gdquest_vse.sync_titles'
    bl_label = 'Synchronize titles'
    bl_description = 'Snap the selected image or text strips to the \
                      corresponding title marker. The marker and strip names \
                      have to start with 1-, 2-, 3-...'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        from re import compile as re_compile

        re_title = re_compile(r'^[0-9]-*')

        title_markers = []
        for marker in bpy.context.scene.timeline_markers:
            if re_title.match(marker.name):
                title_markers.append(int(marker.name[0]), marker.frame)

        for s in bpy.context.selected_sequences:
            if re_title.match(s.name):
                title_id = int(s.name[0])
                for marker in title_markers:
                    if marker[0] == title_id:
                        s.frame_start = marker[1]
                        break
        return {'FINISHED'}


# class AddTitleMarker(bpy.types.Operator):
#     bl_idname = 'gdquest_vse.add_title_marker'
#     bl_label = 'Add title marker'
#     bl_description = 'Add a marker that starts with a number and a dash, \
#                       to use with the Synchronize title operator.'
#     bl_options = {'REGISTER', 'UNDO'}

#     @classmethod
#     def poll(cls, context):
#         return True

#     def execute(self, context):
#         return {'FINISHED'}


# class CreateTitles(bpy.types.Operator):
#     bl_idname = 'gdquest_vse.create_titles'
#     bl_label = 'Create titles with Text strips'
#     bl_description = 'Generates title cards using text strips'
#     bl_options = {'REGISTER', 'UNDO'}

#     @classmethod
#     def poll(cls, context):
#         return True

#     def execute(self, context):
#         return {'FINISHED'}


# TODO: Make it work
# TODO: Access font folders
# TODO: allow to define favorite fonts in add-on prefs
# class AddSimpleText(bpy.types.Operator):
#     """Adds a text strip and sets it up to quickly add an animated note on the video"""
#     bl_idname = "gdquest_vse.add_simple_text"
#     bl_label = "Add a text strip and set it up quickly"
#     bl_options = {'REGISTER', 'UNDO'}

#     strip_duration = IntProperty(
#         name="Duration",
#         description="Length of the text strip in frames"
#         default=96
#     )
#     text = StringProperty(
#         name="Text",
#         description="The text to display on screen"
#         default="Text"
#     )
#     align_x = EnumProperty(
#         items= [('left', 'left', 'Align to the left edge of the screen'),
#                 ('middle', 'middle', 'Align to the middle of the screen'),
#                 ('right', 'right', 'Align to the right edge of the screen')],
#         name="Horizontal align",
#         description="",
#         default='right'
#     )
#     align_y = EnumProperty(
#         items= [('top', 'top', 'Align to the top edge of the screen'),
#                 ('middle', 'middle', 'Align to the middle of the screen'),
#                 ('bottom', 'bottom', 'Align to the bottom edge of the screen')],
#         name="Vertical align",
#         description="",
#         default='right'
#     )
#     animate = BoolProperty(
#         name="Animate opacity",
#         description="",
#         default=True
#     )

#     @classmethod
#     def poll(cls, context):
#         return True

#     def execute(self, context):
#         sequencer = bpy.ops.sequencer
#         current_frame = bpy.context.scene.frame_current

#         sequencer.effect_strip_add(
# type='TEXT', frame_end=current_frame + self.strip_duration,
# replace_sel=True)

#         text_strip = bpy.context.selected_sequences[0]

#         init_text(text_strip, self.text, self.align_x, self.align_y, self.animate)

#         def init_text(sequence, text, align_x, align_y, animate):
#             sequence.name, sequence.text = text

#             sequence.location = (0.0, 0.0)

#             # FONT
#             # ADD TRANSFORM
#             # ADD FADE
#             if animate:
#                 pass

#             return True

#         return {"FINISHED"}