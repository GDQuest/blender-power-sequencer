"""A module to create and synchronize titles for videos,
using timeline markers, and either Image strips or Text strips"""
import bpy


# TODO: Replace with VSE scene import system (import predefined text)
# TODO: Access font folders
# TODO: allow to define favorite fonts in add-on prefs
# class AddSubtitle(bpy.types.Operator):
#     """Adds a text strip and sets it up to quickly add an animated note on the video"""
#     bl_idname = "power_sequencer.add_simple_text"
#     bl_label = "PS - Add a text strip and set it up quickly"
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
