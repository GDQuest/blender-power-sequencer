import os
import bpy
import json
from bpy.props import BoolProperty, IntProperty

from .functions.global_settings import Extensions
from .functions.sequences import find_empty_channel


class ImportLocalFootage(bpy.types.Operator):
    bl_idname = "power_sequencer.import_local_footage"
    bl_label = "PS.Import local footage"
    bl_description = "Import video and audio from the project \
                      folder to VSE strips"

    bl_options = {'REGISTER', 'UNDO'}

    SEQUENCER_AREA = None
    import_all = BoolProperty(
        name="Always Reimport",
        description="If true, always import all local files to new strips. \
                    If False, only import new files (check if footage has \
                    already been imported to the VSE).",
        default=False)
    keep_audio = BoolProperty(
        name="Keep audio from video files",
        description="If False, the audio that comes with video files \
                     will not be imported",
        default=True)

    img_length = IntProperty(
        name="Image strip length",
        description="Controls the duration of the imported image strip",
        default=96,
        min=1)
    img_padding = IntProperty(
        name="Image strip padding",
        description="Padding added between imported image strips in frames",
        default=24,
        min=1)

    start_fps, start_fps_base = None, None
    new_fps, new_fps_base = None, None
    warnings = []

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if not bpy.data.is_saved:
            self.report(
                {'ERROR_INVALID_INPUT'},
                'You need to save your project first. Import cancelled.')
            return {'CANCELLED'}
        sequencer = bpy.ops.sequencer
        context = bpy.context

        bpy.ops.screen.animation_cancel(restore_frame=True)
        self.SEQUENCER_AREA = self.get_sequencer_area()

        project_directory = os.path.split(bpy.data.filepath)[0]
        folders_to_import = [
            f for f in os.listdir(project_directory)
            if f in ('audio', 'img', 'video')
        ]
        local_footage_files = self.find_local_footage_files(
            project_directory, folders_to_import, Extensions.DICT)
        # print('Project dir: {!s},\nFolders found: {!s},\nLocal files: {!s}'.format(project_directory, folders_to_import, local_footage_files))

        files_to_import = self.find_new_files_to_import(local_footage_files)
        if not files_to_import:
            self.report({'INFO'}, "No new files to import found")
            return {'FINISHED'}
        # print('Files to import: {!s}'.format(files_to_import))

        imported_sequences, imported_video_sequences = [], []
        import_channel = find_empty_channel()
        imported_videos_have_audio = False

        self.warnings = []
        self.start_fps, self.start_fps_base = bpy.context.scene.render.fps, bpy.context.scene.render.fps_base
        if 'audio' in files_to_import.keys():
            imported = self.import_audio(
                project_directory, files_to_import['audio'], import_channel)
            imported_sequences.extend(imported)
        if 'video' in files_to_import.keys():
            imported, self.warnings = self.import_videos(
                project_directory, files_to_import['video'],
                import_channel + 1)
            imported_sequences.extend(imported)
            imported_video_sequences.extend(imported)
            if len(imported_video_sequences) > len(files_to_import['video']):
                imported_videos_have_audio = True
        if 'img' in files_to_import.keys():
            img_import_channel = import_channel + 2 + int(
                imported_videos_have_audio)
            imported = self.import_img(
                project_directory, files_to_import['img'], img_import_channel)
            imported_sequences.extend(imported)

        bpy.data.texts['POWER_SEQUENCER_IMPORTS'].from_string(
            json.dumps(local_footage_files))

        self.new_fps, self.new_fps_base = bpy.context.scene.render.fps, bpy.context.scene.render.fps_base

        if imported_videos_have_audio:
            sequencer.select_all(action='DESELECT')
            for s in imported_video_sequences:
                s.select = True
            sequencer.meta_make()
            sequencer.meta_toggle()

            videos_in_meta = [
                s for s in bpy.context.selected_sequences if s.type == 'MOVIE'
            ]
            for s in videos_in_meta:
                s.channel += 2
            for s in imported_video_sequences:
                s.channel -= 1
            sequencer.meta_toggle()
            sequencer.meta_separate()

        for s in [s for s in imported_sequences if s.type == 'SOUND']:
            s.show_waveform = True

        for s in imported_sequences:
            s.select = True

        if self.warnings:
            context.window_manager.invoke_popup(self)
        else:
            self.report({'INFO'},
                        "Imported {!s} strips from newly found files.".format(
                            len(imported_sequences)))
        return {'FINISHED'}

    def draw(self, context):
        start_framerate, new_framerate = 0, 0
        if self.new_fps != self.start_fps or self.new_fps_base != self.start_fps_base:
            start_framerate = round(self.start_fps / self.start_fps_base, 2)
            new_framerate = round(self.new_fps / self.new_fps_base, 2)

        self.layout.label("Import warnings", icon='ERROR')

        if start_framerate and new_framerate:
            self.layout.label("The project's framerate changed")
            self.layout.label(
                "from {} to {}".format(start_framerate, new_framerate))
            self.layout.separator()

        if self.warnings:
            box = self.layout.box()
            box.label("These files' framerate differs")
            box.label("from the project's framerate:")
            for file_name in self.warnings:
                box.label(file_name, icon='FILE_MOVIE')

            self.layout.separator()

            self.layout.label("Blender doesn't support files with")
            self.layout.label("different framerates in the same scene.")
            self.layout.label("Check the source files' framerate")
            self.layout.label("and transcode them with ffmpeg.")

    def get_sequencer_area(self):
        """
        Finds and returns the sequencer area to use as a context override in some operators
        """
        SEQUENCER_AREA = None
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if not area.type == 'SEQUENCE_EDITOR':
                    continue
                SEQUENCER_AREA = {
                    'window': window,
                    'screen': window.screen,
                    'area': area,
                    'scene': bpy.context.scene
                }
        return SEQUENCER_AREA

    def find_local_footage_files(self, project_directory, folders_to_import,
                                 file_extensions):
        """
        Walks through a folder relative to the project directory and returns a list of filepaths that match the extensions.

        Args:
            - project_directory, the absolute path to the folder that contains the .blend file
            - folders_to_import, a list of folder names to look into, relative to the project_directory
            - file_extensions is a dict of tuples of extensions with the form "*.ext".
        Use the Extensions helper class in .functions.global_settings. It gives default extensions to check the files against.

        Returns a dict with the form {
            'video': [relative_path_1, relative_path_2],
            'audio': [...],
            ...
        }
        """
        local_footage_files = {}
        for f in folders_to_import:
            local_footage_files[f] = []
            for root, dirs, files in os.walk(
                    os.path.join(project_directory, f)):
                for ignore_pattern in ('BL_proxy', 'src'):
                    if ignore_pattern in dirs:
                        dirs.remove(ignore_pattern)
                relative_file_paths = [
                    os.path.relpath(
                        os.path.join(root, name), start=project_directory)
                    for name in files
                ]
                local_footage_files[f].extend(relative_file_paths)
        return local_footage_files

    def create_text_file(self, name):
        """
        Create a new text file, change its name and return it
        Args:
        - name, a string to use as the new text file's name"""
        import re
        bpy.ops.text.new()
        re_text = re.compile(r'^Text.[0-9]{3}$')

        text_name = ''
        text_index, max_index = 0, 0
        for text in bpy.data.texts:
            if re_text.match(text.name):
                text_index = int(text.name[-3:])
                if text_index > max_index:
                    max_index = text_index
                    text_name = text.name
        if not text_name:
            text_name = 'Text'

        bpy.data.texts[text_name].name = name
        return bpy.data.texts[name]

    def get_import_text_file_content(self):
        import_text_file = bpy.data.texts.get('POWER_SEQUENCER_IMPORTS')
        if not import_text_file:
            import_text_file = self.create_text_file('POWER_SEQUENCER_IMPORTS')
        content = import_text_file.as_string()
        return content

    def find_new_files_to_import(self, files_dict):
        imported_files_text = self.get_import_text_file_content()
        imported_files = json.loads(
            imported_files_text) if imported_files_text else {}
        files_to_import = {}
        for key in files_dict.keys():
            if key not in imported_files:
                files_to_import[key] = files_dict[key]
                continue
            files_to_import[key] = [
                p for p in files_dict[key]
                if p not in set(imported_files[key])
            ]
            imported_files[key].extend(files_to_import[key])
        return files_to_import

    def import_videos(self, project_directory, videos_to_import,
                      import_channel):
        """
        Imports a list of files using movie_strip_add
        Checks if the scene's framerate changes after importing the strips
        and if the video and audio strips' lengths are different,
        in which case it means the framerate is different from the Blender project

        Returns the list of imported sequences and
        an optional warning message if strips don't follow the project's fps
        """
        video_import_channel = import_channel + 1 if self.keep_audio else import_channel
        import_frame = bpy.context.scene.frame_current

        imported_sequences, warnings = [], []
        for index, f in enumerate(videos_to_import):
            is_first_import = index == 0
            video_file_path = os.path.join(project_directory, f)
            bpy.ops.sequencer.movie_strip_add(
                self.SEQUENCER_AREA,
                filepath=video_file_path,
                frame_start=import_frame,
                channel=video_import_channel,
                sound=self.keep_audio,
                use_framerate=is_first_import)
            imported_sequences.extend(bpy.context.selected_sequences)
            import_frame = bpy.context.selected_sequences[0].frame_final_end

            # FIX audio strip with 1 extra frame
            audio_strip = None
            video_strip = None
            for s in bpy.context.selected_sequences:
                if s.type == 'SOUND':
                    audio_strip = s
                elif s.type == 'MOVIE':
                    video_strip = s

            if not audio_strip:
                continue
            strips_duration_difference = abs(audio_strip.frame_final_end -
                                             video_strip.frame_final_end)
            if strips_duration_difference == 1:
                audio_strip.frame_final_end = video_strip.frame_final_end
            # TODO: defer warnings to the end of the operator's code
            # Return a tuple of video, audio strip so you can compare them later
            elif strips_duration_difference > 1:
                warnings.append(bpy.path.basename(video_strip.filepath))
        return imported_sequences, warnings

    def import_audio(self, project_directory, audio_files, import_channel):
        """
        Imports audio files as sound strips from absolute file paths
        Returns the list of newly imported audio files
        """
        import_frame = bpy.context.scene.frame_current
        new_sequences = []
        for f in audio_files:
            audio_abs_path = os.path.join(project_directory, f)
            bpy.ops.sequencer.sound_strip_add(
                self.SEQUENCER_AREA,
                filepath=audio_abs_path,
                frame_start=import_frame,
                channel=import_channel)
            new_sequences.extend(bpy.context.selected_sequences)
            import_frame = bpy.context.selected_sequences[0].frame_final_end
        return new_sequences

    def import_img(self, project_directory, img_files, import_channel):
        import_frame = bpy.context.scene.frame_current
        new_sequences = []
        for f in img_files:
            head, tail = os.path.split(f)
            img_directory = os.path.join(project_directory, head)
            img_file_dict = [{'name': tail}]
            bpy.ops.sequencer.image_strip_add(
                self.SEQUENCER_AREA,
                directory=img_directory,
                files=img_file_dict,
                frame_start=import_frame,
                frame_end=import_frame + self.img_length,
                channel=import_channel)
            import_frame += self.img_length + self.img_padding
            new_sequences.extend(bpy.context.selected_sequences)
        return new_sequences
