import os
import bpy
import subprocess

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class GenerateProxies(bpy.types.Operator):
    """
    Generate proxies using `bpsproxy` script. It requires `bpsproxy` 
    installed and in the PATH environment variable.
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'I', 'value': 'PRESS', 'ctrl': True},
             {'keep_audio': True},
             'GenerateProxies')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}
    SEQUENCER_AREA = None

    videos_path = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return len(context.selected_sequences) > 0

    def execute(self, context):
        # TODO: I need to check this
        if not bpy.data.is_saved:
            self.report(
                {'ERROR_INVALID_INPUT'},
                'You need to save your project first. Proxies generation cancelled.')
            return {'CANCELLED'}

        video_directory_path = bpy.path.abspath(context.scene.video_directory)

        # TODO: check if bpsproxy is installed
        # subprocess.call([
        #     'bpsproxy',
        #     video_directory_path
        # ])

        # TODO:
        # if checkbox is ticked
        # then SpaceSequenceEditor.proxy_render_sixe =
        print(bpy.context.space_data)
        print(bpy.context.space_data.proxy_render_size)
        bpy.ops.sequencer.enable_proxies(proxy_25=True)
        print(bpy.context.space_data.proxy_render_size)
        
        # for sequence in context.selected_sequences:
        #     if sequence.type == "MOVIE":
        #         print(sequence)
        #         print(sequence.filepath)
        #         print("\n--------")

        # sequencer = bpy.ops.sequencer
        # project_directory = os.path.split(bpy.data.filepath)[0]

        return {'FINISHED'}
