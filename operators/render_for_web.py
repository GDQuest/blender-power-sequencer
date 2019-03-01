import bpy
import os

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_render_for_web(bpy.types.Operator):
    """
    Render video with good settings for web upload
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'F12', 'value': 'PRESS', 'alt': True},
             {'preset': 'youtube',
              'name_pattern': 'scene',
              'auto_render': True},
             'Render for Web')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {"REGISTER"}

    preset: bpy.props.EnumProperty(
        items=[(
            'youtube', 'youtube',
            'Full HD mp4 with AAC audio, following recommendations from Youtube'
        ), ('twitter', 'twitter',
            'HD ready mp4 with high enough bitrate for Twitter and Facebook')],
        name='Preset',
        description='Preset to use ',
        default='youtube')

    name_pattern: bpy.props.EnumProperty(
        items=[
            ('folder', 'Folder',
             'Use the folder\'s name as the exported file name'),
            ('blender', 'Blender file',
             'Use the project\'s .blend file name as the exported file name'),
            ('scene', 'Current scene',
             'Use the scene\'s name as the exported file name')
        ],
        name="Filename",
        description="Auto name the rendered video after...",
        default='blender')

    auto_render: bpy.props.BoolProperty(
        name="Auto render",
        description="Launch the render automatically",
        default=False)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report({'WARNING'}, "Save your file first")
            return {'CANCELLED'}

        script_file = os.path.realpath(__file__)
        addon_directory = os.path.dirname(script_file)

        # audio
        if context.scene.render.ffmpeg.audio_codec == 'NONE':
            context.scene.render.ffmpeg.audio_codec = 'AAC'
            context.scene.render.ffmpeg.audio_bitrate = 192

        # video
        if self.preset == 'youtube':
            bpy.ops.script.python_file_run(filepath=os.path.join(
                addon_directory, 'render_presets', 'youtube_1080.py'))
        elif self.preset == 'twitter':
            bpy.ops.script.python_file_run(filepath=os.path.join(
                addon_directory, 'render_presets', 'twitter_720p.py'))

        from os.path import splitext, dirname
        path = bpy.data.filepath

        exported_file_name = 'video'
        if self.name_pattern == 'blender':
            exported_file_name = splitext(bpy.path.basename(path))[0]
        elif self.name_pattern == 'folder':
            exported_file_name = dirname(path).rsplit(sep="\\", maxsplit=1)[-1]
        elif self.name_pattern == 'scene':
            exported_file_name = context.scene.name

        context.scene.render.filepath = "//" + exported_file_name + '.mp4'

        if self.auto_render:
            bpy.ops.render.render(
                {
                    'dict': "override"
                }, 'INVOKE_DEFAULT', animation=True)
            self.report({'INFO'}, 'Rendering {!s} with the {!s} preset'.format(
                exported_file_name, self.preset))
        else:
            self.report(
                {'INFO'},
                'Render settings set to the {!s} preset'.format(self.preset))
        return {"FINISHED"}

