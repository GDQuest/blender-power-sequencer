import os
import bpy

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

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report(
                {'ERROR_INVALID_INPUT'},
                'You need to save your project first. Proxies generation cancelled.')
            return {'CANCELLED'}
            
        print("TODO: Executing bpsproxy")
        # sequencer = bpy.ops.sequencer
        # project_directory = os.path.split(bpy.data.filepath)[0]
    
        return {'FINISHED'}