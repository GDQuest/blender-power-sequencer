import bpy
import os
from multiprocessing import Process, Queue

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description

from bpsproxy.call import call


# def something(clargs):
#     tools = ['ffmpeg']
#     try:
#         checktools(tools)
#         n, path_i = find_files(clargs.working_directory)
#         kwargs = {'path_i': path_i,
#                   'n': n}
#         call_makedirs(C, clargs, **kwargs)
#         call(C, clargs, cmds=get_commands_all(C, clargs, **kwargs), **kwargs)
#     except ToolError as e:
#         print(e)


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
    _queue = Queue()
    _proxy_rendered = -1
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
        self._timer = wm.event_timer_add(0.02, context.window)
        # update Class variable to keep track of the state
        GenerateProxies.running = True
        return {'RUNNING_MODAL'}

    def run_bpsproxy(self, context):
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

        p = Process(target=self.generate_proxies, args=("test",))
        p.start()
        p.join()

        return {'FINISHED'}


    def generate_proxies(self, args_tuple):
        print(args_tuple)
        import time
        time.sleep(0.5)
        self._queue.put(1)


    def modal(self, context, event):
        """ This method is called continuosly when`execute` returns {"RUNNING_MODAL"}.
        It's not called at all in other cases.
        It stops being executed when it returns {"FINISHED"}
        """
        if event.type == "TIMER":
            print("TIMER")
            wm = context.window_manager
            # check if bpsproxy rendered everything
            try:
                self._proxy_rendered = self._queue.get(block=False)
            except Exception as e:
                print(e)
            # if value is greater than 0, bpsproxy process completed correctly
            if self._proxy_rendered> 0:
                print(self._proxy_rendered)
                print("FINISHED!")
            else:
                print("PROXYYYY")

            if GenerateProxies.fake_progress < 100:
                GenerateProxies.fake_progress += 1
                wm.progress_update(GenerateProxies.fake_progress)
            else:
                wm.progress_end()
                GenerateProxies.running = False 
                GenerateProxies.fake_progress = 0
                return {'FINISHED'}
        return {'PASS_THROUGH'}
