import bpy

from bpy_extras.io_utils import ExportHelper

class ExportSequence(bpy.types.Operator, ExportHelper):
    bl_idname = "power_sequencer.export_sequence"
    bl_label = "Export Sequence"
    bl_description = "Export current Sequence"
    filename_ext = ""
    filepath = bpy.props.StringProperty()
    
    #for integration of multithread rendering
    #regular=bpy.props.BoolProperty(name='Regular Render', default=False)
        
    @classmethod
    def poll(cls, context):
        return bpy.context.area.type=='SEQUENCE_EDITOR' and bpy.context.scene.sequence_editor is not None and bpy.data.is_saved==True
    
    def draw(self, context):
        layout = self.layout
        
        rd = context.scene.render
        image_settings = rd.image_settings
        file_format = image_settings.file_format
        ffmpeg = rd.ffmpeg
        
        ### for integration of multithread rendering ###
        #layout.prop(self, "regular")
        
        box=layout.box()
        
        split = box.split()

        col = split.column()
        col.active = not rd.is_movie_format
        col.prop(rd, "use_overwrite")
        col.prop(rd, "use_placeholder")

        col = split.column()
        col.prop(rd, "use_file_extension")
        col.prop(rd, "use_render_cache")
    
        box.template_image_settings(image_settings, color_management=False)
        if rd.use_multiview:
            box.template_image_views(image_settings)

        if file_format == 'QUICKTIME':
            quicktime = rd.quicktime

            split = box.split()
            col = split.column()
            col.prop(quicktime, "codec_type", text="Video Codec")
            col.prop(quicktime, "codec_spatial_quality", text="Quality")

            # Audio
            col.prop(quicktime, "audiocodec_type", text="Audio Codec")
            if quicktime.audiocodec_type != 'No audio':
                split = box.split()
                if quicktime.audiocodec_type == 'LPCM':
                    split.prop(quicktime, "audio_bitdepth", text="")

                split.prop(quicktime, "audio_samplerate", text="")

                split = box.split()
                col = split.column()
                if quicktime.audiocodec_type == 'AAC':
                    col.prop(quicktime, "audio_bitrate")

                subsplit = split.split()
                col = subsplit.column()

                if quicktime.audiocodec_type == 'AAC':
                    col.prop(quicktime, "audio_codec_isvbr")

                col = subsplit.column()
                col.prop(quicktime, "audio_resampling_hq")
                
        if file_format=='FFMPEG':
            box.menu("RENDER_MT_ffmpeg_presets", text="Presets")

            split = box.split()
            split.prop(rd.ffmpeg, "format")
            split.prop(ffmpeg, "use_autosplit")

            box.separator()

            needs_codec = ffmpeg.format in {'AVI', 'QUICKTIME', 'MKV', 'OGG', 'MPEG4'}
            if needs_codec:
                box.prop(ffmpeg, "codec")

            if ffmpeg.codec in {'DNXHD'}:
                box.prop(ffmpeg, "use_lossless_output")

            # Output quality
            if needs_codec and ffmpeg.codec in {'H264', 'MPEG4'}:
                box.prop(ffmpeg, "constant_rate_factor")

            # Encoding speed
            box.prop(ffmpeg, "ffmpeg_preset")
            # I-frames
            box.prop(ffmpeg, "gopsize")
            # B-Frames
            row = box.row()
            row.prop(ffmpeg, "use_max_b_frames", text='Max B-frames')
            pbox = row.split()
            pbox.prop(ffmpeg, "max_b_frames", text='')
            pbox.enabled = ffmpeg.use_max_b_frames

            split = box.split()
            split.enabled = ffmpeg.constant_rate_factor == 'NONE'
            col = split.column()
            col.label(text="Rate:")
            col.prop(ffmpeg, "video_bitrate")
            col.prop(ffmpeg, "minrate", text="Minimum")
            col.prop(ffmpeg, "maxrate", text="Maximum")
            col.prop(ffmpeg, "buffersize", text="Buffer")

            col = split.column()
            col.label(text="Mux:")
            col.prop(ffmpeg, "muxrate", text="Rate")
            col.prop(ffmpeg, "packetsize", text="Packet Size")

            box.separator()

            # Audio:
            if ffmpeg.format != 'MP3':
                box.prop(ffmpeg, "audio_codec", text="Audio Codec")

            row = box.row()
            row.enabled = ffmpeg.audio_codec != 'NONE'
            row.prop(ffmpeg, "audio_bitrate")
            row.prop(ffmpeg, "audio_volume", slider=True)
    
    def execute(self, context):
        bpy.context.scene.render.filepath = filepath
        
        ### for integration of multithread rendering ###
        #if self.regular==True:
        #else:
        
        bpy.ops.render.opengl(animation=True, sequencer=True)
        return {'FINISHED'}
