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

        sizes = []
        bpsproxy_command = ['bpsproxy', video_directory_path]

        if context.scene.proxy_25:
            sizes.append("25")
        if context.scene.proxy_50:
            sizes.append("50")
        if context.scene.proxy_100:
            sizes.append("100")        
        if len(sizes) > 0:
            bpsproxy_command.extend(['-s', *sizes])
        if context.scene.proxy_preset:
            bpsproxy_command.extend(['-p', context.scene.proxy_preset])
        # debug print
        print(bpsproxy_command)

        # TODO: check if bpsproxy is installed

        subprocess.call(bpsproxy_command)
        
        # TODO: check for command completion rate
        
        # for sequence in context.selected_sequences:
        #     if sequence.type == "MOVIE":
        #         print(sequence)
        #         print(sequence.filepath)
        #         print("\n--------")

        # sequencer = bpy.ops.sequencer
        # project_directory = os.path.split(bpy.data.filepath)[0]

        return {'FINISHED'}
