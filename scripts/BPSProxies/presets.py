"""
Presets provided by François Grassard. Reference commands:
    ffmpeg -i input.mov -pix_fmt yuv420p -crf 25 -c:v libvpx -speed 16 \
    -g 1 -threads 8 -vf colormatrix=bt601:bt709 output.webm
    ffmpeg -i input.mov -pix_fmt yuv420p -crf 25 -preset veryslow \
    -g 1 -vf colormatrix=bt601:bt709 output.mp4

For detailed information, see:
https://github.com/GDquest/Blender-power-sequencer/issues/174#issuecomment-420586813

"""
MP4_DEFAULTS = {
    'format': 'mp4',
    'codec': 'libx264',
    'crf': 25,
    'encoding_speed': {
        'key': "-preset",
        'value': "faster",
    },
}
WEBM_DEFAULTS = {
    'format': 'webm',
    'codec': "libvpx",
    'crf': 25,
    'encoding_speed': {
        'key': "-speed",
        'value': 16,
    },
}
NVENC_DEFAULTS = {
    'format': 'mp4',
    'codec': "h264_nvenc",
    'crf': 25,
    'encoding_speed': {
        'key': "-preset",
        'value': "fast",
    },
}
PRESETS = {
    'mp4': MP4_DEFAULTS,
    'webm': WEBM_DEFAULTS,
    'nvenc': NVENC_DEFAULTS
}
