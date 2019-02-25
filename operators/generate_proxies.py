import bpy
import os
from multiprocessing import Process, Queue

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description

from bpsproxy.call import call


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
        # enable GUI buttons only if the operator is not generating proxies
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
        # update class variable to keep track of the state
        GenerateProxies.running = True
        print(GenerateProxies.running)
        return {'RUNNING_MODAL'}

    def run_bpsproxy(self, context):
        """ Prepare arguments for bpsproxy taking them from the Blender GUI and call a method
        responsible to communicate with bpsproxy module."""
        bpsproxy_args = {}
        # get selected sizes
        sizes = []
        if context.scene.proxy_25:
            sizes.append("25")
        if context.scene.proxy_50:
            sizes.append("50")
        if context.scene.proxy_100:
            sizes.append("100")
        # populate bpsproxy_args dict
        bpsproxy_args["video_dir_path"] = bpy.path.abspath(
            context.scene.video_directory
        )
        if len(sizes) > 0:
            bpsproxy_args["sizes"] = ["-s", *sizes]
        if context.scene.proxy_preset:
            bpsproxy_args["proxy_preset"] = ['-p', context.scene.proxy_preset]

        # create a process and spawn it
        p = Process(target=self.generate_proxies, args=(bpsproxy_args,))
        p.start()

        return {'FINISHED'}

    def generate_proxies(self, bpsproxy_args):
        """ Start the generation of proxies using methods from bpsproxy module """
        print(bpsproxy_args)
        # take a coffee for 2 secs
        import time
        time.sleep(2)
        # call(config, clargs, cmds, kwargs)

        # put data in the queue, so that it can be read from modal()
        self._queue.put(1)

    def modal(self, context, event):
        """ This method is called continuosly when`execute` returns {"RUNNING_MODAL"}.
        It's not called at all in other cases.
        It stops being executed when it returns {"FINISHED"}
        """
        if event.type == "TIMER":
            wm = context.window_manager
            # check if bpsproxy rendered everything
            try:
                self._proxy_rendered = self._queue.get(block=False)
            except Exception as e:
                print(e)
            # if value is 1, bpsproxy process completed correctly
            if self._proxy_rendered == 1:
                print(self._proxy_rendered)
                print("Proxies generated.")
            else:
                print("Generating proxies...")

            if GenerateProxies.fake_progress < 100:
                # update Blender progress GUI
                GenerateProxies.fake_progress += 1
                wm.progress_update(GenerateProxies.fake_progress)
            else:
                wm.progress_end()
                GenerateProxies.running = False
                GenerateProxies.fake_progress = 0
                return {'FINISHED'}
        return {'PASS_THROUGH'}
