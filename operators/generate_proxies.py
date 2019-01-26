import bpy
import os
import subprocess
import threading

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
        if not bpy.data.is_saved:
            self.report(
                {'ERROR_INVALID_INPUT'},
                'You need to save your project first. Proxies generation cancelled.')
            return {'CANCELLED'}

        video_directory_path = bpy.path.abspath(context.scene.video_directory)

        # TODO: check if bpsproxy is installed
        # eg: Blender does not take environment variable from user configuration like .bashrc or .zshrc
        # I have ~/.local/bin exported in my zshrc file and I can use bpsproxy from the console, but Blender doesn't
        # unless executed from the console.
        # 
        # https://unix.stackexchange.com/questions/81243/how-do-i-set-the-path-or-other-environment-variables-so-that-x-apps-can-access-i
        subprocess.call(["printenv", "PATH"])
        bpsproxy_command = ['bpsproxy', video_directory_path]
        sizes = []

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

        # TODO: progress update
        wm = bpy.context.window_manager
        tot = 10000000
        wm.progress_begin(0, tot)
        update_gui_thread = threading.Thread(target=update_progress, args=(wm, tot))
        update_gui_thread.start()

        execute_bpsproxy = lambda shell_cmd: subprocess.Popen(shell_cmd)
        bpsproxy_thread = threading.Thread(target=execute_bpsproxy, args=([bpsproxy_command]))
        bpsproxy_thread.start()

        return {'FINISHED'}


def update_progress(wm, tot):
    import time
    for i in range(tot):
        wm.progress_update(i)
    wm.progress_end()