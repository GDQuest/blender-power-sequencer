import bpy
from bpy.app.handlers import persistent


class PowerSequencerProps(bpy.types.PropertyGroup):
    playback_speed = bpy.props.EnumProperty(
        items=[('normal', 'Normal (1x)', ''),
        ('fast', 'Fast (1.33x)', ''),
        ('faster', 'Faster (1.66x)', ''),
        ('double', 'Double (2x)', ''),
        ('triple', 'Triple (3x)', '')],
        name = 'Playback speed',
        default='double')
    frame_pre = bpy.props.IntProperty(
        name = 'Frame before frame_change',
        default = 0,
        min = 0)

class ChangePlaybackSpeed(bpy.types.Operator):
    """
    Change the playback_speed property using an operator property.
    Used with keymaps
    """
    bl_idname = "power_sequencer.change_playback_speed"
    bl_label = "PS.Change playback speed"
    bl_description = "Change the playback speed"

    bl_options = {"REGISTER"}

    speed = bpy.props.EnumProperty(
        items=[('normal', 'Normal (1x)', ''),
        ('fast', 'Fast (1.33x)', ''),
        ('faster', 'Faster (1.66x)', ''),
        ('double', 'Double (2x)', ''),
        ('triple', 'Triple (3x)', '')],
        name='Speed',
        description='Change the playback speed',
        default='double')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.scene.power_sequencer.playback_speed = self.speed
        return {"FINISHED"}


@persistent
def load_file_post(arg):
    """
    Called after loading the blend file
    """
    for scene in bpy.data.scenes:
        scene.power_sequencer.frame_pre = bpy.context.scene.frame_current


# TODO: if change speed with mouse, don't process
# TODO: support going back in time with arrow keys and play
# Options: wrap bpy.ops.screen.frame_offset etc.?
@persistent
def playback_speed_post(scene):
    """
    Handler function for faster playback
    Skips keyframes after a frame change based on the playback_speed value
    It steps over frame rather than increase the playback speed smoothly,
    but it's still useful for faster editing
    """
    if not bpy.context.screen.is_animation_playing:
        return

    scene = bpy.context.scene
    playback_speed = scene.power_sequencer.playback_speed

    frame_pre = scene.power_sequencer.frame_pre
    frame_multipler = 1
    # FIXME: problem is that if playback_speed > 0,
    # frame_pre is > frame_current even if the user went back in time
    # Must take in account all speed levels
    # if frame_pre < scene.frame_current:
    #   frame_multipler = -1
    # Only need to work for backwards playback

    if playback_speed == 'fast' and scene.frame_current % 3 == 0:
        scene.frame_current = scene.frame_current + 1 * frame_multipler
    elif playback_speed == 'faster' and scene.frame_current % 2 == 0:
        scene.frame_current = scene.frame_current + 1 * frame_multipler
    elif playback_speed == 'double':
        # 2.5x -> skip 5 frames for 2. 2 then 3 then 2 etc.
        scene.frame_current = scene.frame_current + 1 * frame_multipler
    elif playback_speed == 'triple':
        scene.frame_current = scene.frame_current + 2 * frame_multipler

    print('Pre {!s} / Post {!s}'.format(frame_pre, scene.frame_current))
    scene.power_sequencer.frame_pre = scene.frame_current


def draw_playback_speed(self, context):
    layout = self.layout
    scene = context.scene
    layout.prop(scene.power_sequencer, 'playback_speed')


def handlers_register():
    # MENUS
    bpy.types.SEQUENCER_HT_header.append(draw_playback_speed)

    # HANDLERS
    load_post = bpy.app.handlers.load_post
    for handler in load_post:
        if (" load_file_post " in str(handler)):
            load_post.remove(handler)
    load_post.append(load_file_post)

    frame_change_post = bpy.app.handlers.frame_change_post
    for handler in frame_change_post:
        if (" playback_speed_post " in str(handler)):
            frame_change_post.remove(handler)
    frame_change_post.append(playback_speed_post)



def handlers_unregister():
    # MENUS
    bpy.types.SEQUENCER_HT_header.remove(draw_playback_speed)

    # HANDLERS
    load_post = bpy.app.handlers.load_post
    for handler in load_post:
        if (" load_file_post " in str(handler)):
            load_post.remove(handler)

    frame_change_post = bpy.app.handlers.frame_change_post
    for handler in frame_change_post:
        if (" playback_speed_post " in str(handler)):
            frame_change_post.remove(handler)
