import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class AddTransform(bpy.types.Operator):
    """
    *brief* Add transform effect to selected image and movie strips. Auto centers images


    For each strip in the selection:

    * Filters the selection down to image and movie strips
    * Centers the pivot point of image strips
    * Adds a transform effect and sets it to ALPHA_OVER
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'T', 'value': 'PRESS'}, {}, 'Add Transform')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            next((s for s in context.selected_sequences if s.type in ('IMAGE', 'MOVIE')))
            return True
        except StopIteration:
            return False

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        sequence_editor = context.scene.sequence_editor
        render = context.scene.render

        selection = context.selected_sequences
        selection = [s for s in selection if s.type in ('IMAGE', 'MOVIE')]
        if not selection:
            self.report({"ERROR_INVALID_INPUT"},
                        "No sequences movie or image strips selected")
            return {'CANCELLED'}

        transform_strips = []
        sequencer.select_all(action='DESELECT')
        image_strips = [s for s in selection if s.type == 'IMAGE']

        # Center image strips pivot
        for s in image_strips:
            if s.use_translation and (s.transform.offset_x != 0 or
                                      s.transform.offset_y != 0):
                continue

            image_width = s.elements[0].orig_width
            image_height = s.elements[0].orig_height
            if image_width == 0 or image_height == 0:
                raise ValueError('image_height or image_width is 0')

            # image_ratio = image_width / image_height
            # render_ratio = render.resolution_x / render.resolution_y
            # if image_ratio != render_ratio:
            #     continue

            if image_width < render.resolution_x or image_height < render.resolution_y:
                s.use_translation = True
                s.transform.offset_x = (render.resolution_x - image_width) / 2
                s.transform.offset_y = (render.resolution_y - image_height) / 2

        # Add a transform effect to all selected MOVIE and IMAGE strips
        for s in selection:
            sequence_editor.active_strip = s
            sequencer.effect_strip_add(type='TRANSFORM')

            active = sequence_editor.active_strip
            active.name = "TRANSFORM-{!s}".format(s.name)
            active.blend_type = 'ALPHA_OVER'
            transform_strips.append(active)
            active.select = False
            s.mute = True

        # Select img strips and transform effects
        for s in transform_strips:
            s.select = True
        for s in selection:
            s.select = True
        sequence_editor.active_strip = transform_strips[0]
        self.report({"INFO"}, "Successfully processed " + str(len(selection)) +
                    " image sequences")
        return {'FINISHED'}

