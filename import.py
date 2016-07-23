import bpy
import os

def find_empty_channel(mode = 'ABOVE'):
    """Finds and returns the first empty channel in the VSE
    Takes the optional argument mode: 'ABOVE' or 'ANY'
    'ABOVE' finds the first empty channel above all of the other strips
    'ANY' finds the first empty channel, even if there are strips above it"""

    sequencer = bpy.ops.sequencer
    sequences = bpy.context.sequences

    channels = []
    empty_channel = -1

    # If there is no sequence in the VSE, the first channel is empty, so we return 0
    if not sequences:
        return 1

    for s in bpy.context.sequences:
        # Add the channels of all sequences to a list
        channels.append(s.channel)

    # Remove duplicates by converting channels to a set
    # Convert back to a list and sort the channel numbers
    channels = sorted(list(set(channels)))

    for i in range(50):
        # If the current loopindex is not in the channels list, then the channel is empty
        if i not in channels:
            if mode == 'ANY':
                empty_channel = i
                break
            elif mode == 'ABOVE':
                # Check that there is no value higher than i in channels[]
                if max(channels) < i:
                    empty_channel = i
                    break
    if empty_channel == -1:
        print("No empty channel was found")
        return None
    else:
        return empty_channel


# Changes parameters of the image strips. CALLED BACK ON IMPORT
# Currently: adds transform effect, sets to alpha over
# TODO: Move parameters to PropertyGroup and preferences
# TODO: add option to add fade in and/or out
# TODO: add option to add default animation (ease in/out on X axis) on transform FX
def setup_image_strips(strips = None):
    sequencer = bpy.ops.sequencer
    seq_ed = bpy.context.scene.sequence_editor

    if strips != None:
        # Ensure that no other strip is selected to add FX strips to the right target
        sequencer.select_all(action='DESELECT')

        for s in strips:
            if s.type == 'IMAGE':
                # Set the strip active so that we can
                seq_ed.active_strip = s
                sequencer.effect_strip_add(type='TRANSFORM')
                # The transform strip becomes active and selected
                seq_ed.active_strip.blend_type = 'ALPHA_OVER'
                seq_ed.active_strip.select = False
            else:
                print("The strip " + s.name + " is not an image strip")
        print("Successfully processed " + str(len(strips)) + " image strips")
        return True
    else:
        print("You didn't pass any strips")
        return False




# TODO: optimize to import all strips of a given type at once using a dictionary
# TODO: Do not reimport existing strips, import only the new ones and refresh the sequencer
# TODO: Dive into sub-folders for video strips (i.e. /video/**/*.MTS), 1 level deeper
# TODO: Option to automatically remove audio from the imported video strips (if importing wav audio files)
# TODO: After import, if video and audio files have the same name, remove audio channel from video and sync remaining audio and video strips (if there's audio channel with video)
# TODO: Use preference to change default image length
class ImportLocalFootage(bpy.types.Operator):
    bl_idname = "gdquest_vse.import_local_footage"
    bl_label = "Import local footage"
    bl_description = "Import video and audio from the project folder to VSE strips"
    bl_options = {"REGISTER"}

    always_import = bpy.props.BoolProperty( name = "Always Reimport", description = "If true, always import all local files to new strips. If False, only import new files (check if footage has already been imported to the VSE).", default = False)
    video_keep_audio = bpy.props.BoolProperty( name = "Keep audio from video files", description = "If False, the audio that comes with video files will not be imported", default = False)
    img_length = bpy.props.IntProperty( name = "Image strip length", description = "Controls the duration of the imported image strips length", default = 96, min = 1)

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        sequencer = bpy.ops.sequencer
        context = bpy.context
        wm = context.window_manager

        # Sequencer Area to force Blender to import of the strips to the VSE, even if the current context is not the VSE
        sequencer_area = {'region': wm.windows[0].screen.areas[2].regions[0], 'blend_data': context.blend_data, 'scene': context.scene, 'window': wm.windows[0], 'screen': bpy.data.screens['Video Editing'], 'area': bpy.data.screens['Video Editing'].areas[2]}

        if bpy.data.is_saved:
            path = bpy.data.filepath
            project_name = bpy.path.basename(path)

            # REIMPORT
            # If there are already strips in the VSE, we have to check the names of the imported files against the existing strips to not duplicate them on import
            # Only new video files have to be imported
            # TODO: Make this behavior optional
            # always_import = self.always_import
            # video_keep_audio = self.video_keep_audio
            always_import = True
            video_keep_audio = False
            # If we're keeping the audio channel of the video files, we'll need to offset other audio and img strips by 1 channel
            channel_for_audio = 1 if video_keep_audio else 0
            check_strip_names = False

            if always_import == False and len(context.sequences) > 0:
                for s in context.sequences:
                    if s.type in ['MOVIE', 'SOUND', 'IMAGE']:
                        check_strip_names = True
                        break

            # Store project folder
            directory = path[:len(path) - (len(project_name) + 1)]
            print("\n" + directory)

            # Finds first empty channel above all strips to place the new strips
            empty_channel = find_empty_channel(mode = 'ABOVE')
            # Check if there's a subfolder in the blend project folder named 'video' and loop through content
            for entry in os.listdir(path=directory):
                # VIDEO STRIPS
                if entry == 'video':
                    # Ensure that there is something in the folder
                    video_path = directory + '\\' + 'video'
                    video_folder_content = os.listdir(path=video_path)
                    if len(video_folder_content) > 0:
                        strip_insert_frame = 1
                        video_channel = empty_channel
                        # We have to make a dictionary of video filenames to quickly import
                        videos = []
                        subfolders = []

                        for video in video_folder_content:
                            # If filename is .mp4 or any video format, import to the VSE
                            filename = video.lower()
                            if '.mts' in filename or '.mp4' in filename:
                                if check_strip_names:
                                    for s in context.sequences:
                                        if not video in s.name:
                                            videos.append({ 'name': video })
                                            break
                                else:
                                    videos.append({ 'name': video })
                            # Find and save subfolders of the //video folder, 1 level deep
                            else:
                                subfolder = os.path.join(video_path, video)
                                if os.path.isdir(subfolder):
                                    subfolders.append(subfolder)
                        # Walk through the subfolders and append the videos
                        # TODO: tag the videos strips per folder
                        if subfolders:
                            for folder in subfolders:
                                for video in os.listdir(path = folder):
                                    filename = video.lower()
                                    if '.mts' in filename or '.mp4' in filename:
                                        videos.append({ 'name': os.path.split(folder)[1] + "/" + video })
                        sequencer.movie_strip_add(sequencer_area, filepath = video_path + "\\" + video, files = videos, frame_start = 1, channel = video_channel, sound = video_keep_audio)
                # AUDIO STRIPS
                elif entry == 'audio':
                    audio_folder_content = os.listdir(path=(directory + '\\' + entry))
                    if len(audio_folder_content) > 0:
                        strip_insert_frame = 1
                        # We have to reset the empty_channel and starting frame to add the audio strips
                        audio_channel = empty_channel + 1 + channel_for_audio
                        audio_path = directory + '\\' + 'audio'

                        for audio in audio_folder_content:
                            filename = audio.lower()
                            if '.wav' in filename or '.mp3' in filename:
                                sequencer.sound_strip_add(sequencer_area, filepath = audio_path + "\\" + audio, frame_start = strip_insert_frame, channel = audio_channel)
                                strip_insert_frame += context.sequences[0].frame_final_duration
                # IMAGE STRIPS
                elif entry == 'img':
                    img_folder_content = os.listdir(path=(directory + '\\' + entry))
                    if len(img_folder_content) > 0:
                        strip_insert_frame = 1
                        strip_duration = self.img_length
                        image_channel = empty_channel + 2 + channel_for_audio
                        image_path = directory + '\\' + 'img'

                        for image in img_folder_content:
                            filename = image.lower()
                            if '.jpg' in filename or '.png' in filename:
                                sequencer.image_strip_add(sequencer_area, directory = image_path, files = [{ 'name' : image }], frame_start = strip_insert_frame, frame_end = strip_insert_frame + strip_duration, channel = image_channel)
                                strip_insert_frame += strip_duration + 1

        # store image strips in a list to then process them using the setup_image_strips() function
        image_strips = []
        for s in context.sequences:
            if s.type == 'IMAGE':
                image_strips.append(s)
                pass
        # Process all image strips so that they are ready to be used for editing
        setup_image_strips(image_strips)

        # Deselect all strips
        sequencer.select_all(action='DESELECT')
        return {"FINISHED"}
