import bpy
import os
import subprocess
import threading

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class GenerateProxies(bpy.types.Operator):
    """
    Generate proxies using `bpsproxy` script.
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

    _timer = None
    running = False
    fake_progress = 0

    @classmethod
    def poll(cls, context):
        return GenerateProxies.running == False

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report(
                {'ERROR_INVALID_INPUT'},
                'You need to save your project first. Proxies generation cancelled.')
            return {'CANCELLED'}
        # start bpsproxy in the background
        self.run_bpsproxy(context)
        # Run the operator in "modal" mode, to avoid crashes
        # read more here: https://blender.stackexchange.com/questions/1050/blender-ui-multithreading-progressbar
        wm = context.window_manager
        wm.modal_handler_add(self)
        wm.progress_begin(0, 100)
        # start timer to trigger modal events
        self._timer = wm.event_timer_add(0.25, context.window)
        # update Class variable to keep track of the state
        GenerateProxies.running = True
        return {'RUNNING_MODAL'}

    def run_bpsproxy(self, context):
        # TODO: check if bpsproxy is installed
        # eg: Blender does not take environment variable from 
        # user configuration like .bashrcor .zshrc
        # I have ~/.local/bin exported in my zshrc file and I can 
        # use bpsproxy from the console but Blender doesn't,
        # unless executed from the console.
        # https://unix.stackexchange.com/questions/81243/how-do-i-set-the-path-or-other-environment-variables-so-that-x-apps-can-access-i
        subprocess.call(["printenv", "PATH"])

        video_directory_path = bpy.path.abspath(context.scene.video_directory)
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

        subprocess.Popen(bpsproxy_command)

        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == "TIMER":
            wm = context.window_manager
            if GenerateProxies.fake_progress < 100:
                GenerateProxies.fake_progress += 1
                wm.progress_update(GenerateProxies.fake_progress)
            else:
                wm.progress_end()
                GenerateProxies.running = False 
                GenerateProxies.fake_progress = 0
                return {'FINISHED'}
        return {'PASS_THROUGH'}