import bpy
import bgl
import gpu
from gpu_extras.batch import batch_for_shader
import math
from mathutils import Vector

from .utils.functions import (
    find_strips_mouse,
    trim_strips,
    find_snap_candidate,
    find_closest_surrounding_cuts,
    sequencer_workaround_2_80_audio_bug,
)

from .utils.draw import (
    draw_line,
    draw_rectangle,
    draw_triangle_equilateral,
    draw_arrow_head,
    get_color_gizmo_primary,
    get_color_gizmo_secondary,
)
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description

if not bpy.app.background:
    SHADER = gpu.shader.from_builtin("2D_UNIFORM_COLOR")


class POWER_SEQUENCER_OT_mouse_trim(bpy.types.Operator):
    """
    *brief* Cut or Trim strips quickly with the mouse cursor


    Click somehwere in the Sequencer to insert a cut, click and drag to trim
    With this function you can quickly cut and remove a section of strips while keeping or
    collapsing the remaining gap.

    A [video demo](https://youtu.be/GiLmDhmMVAM?t=1m35s) is available.
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "https://i.imgur.com/wVvX4ex.gif",
        "description": doc_description(__doc__),
        "shortcuts": [
            (
                {"type": "T", "value": "PRESS"},
                {"select_mode": "CONTEXT", "gap_remove": False},
                "Trim using the mouse cursor",
            ),
            (
                {"type": "T", "value": "PRESS", "alt": True},
                {"select_mode": "CONTEXT", "gap_remove": True},
                "Trim using the mouse cursor and remove gaps",
            ),
            (
                {"type": "T", "value": "PRESS", "shift": True},
                {"select_mode": "CURSOR", "gap_remove": True},
                "Trim in all channels",
            ),
            (
                {"type": "T", "value": "PRESS", "shift": True, "alt": True},
                {"select_mode": "CURSOR", "gap_remove": True},
                "Trim in all channels and remove gaps",
            ),
        ],
        "keymap": "Sequencer",
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc["name"]
    bl_description = doc_brief(doc["description"])
    bl_options = {"REGISTER", "UNDO"}

    select_mode: bpy.props.EnumProperty(
        items=[
            ("CURSOR", "Time cursor", "Select all of the strips the time cursor overlaps"),
            ("CONTEXT", "Smart", "Uses the selection if possible, else uses the other modes"),
        ],
        name="Selection mode",
        description="Cut only the strip under the mouse or all strips under the time cursor",
        default="CONTEXT",
    )
    select_linked: bpy.props.BoolProperty(
        name="Use linked time",
        description="In mouse or CONTEXT mode, always cut linked strips if this is checked",
        default=False,
    )
    gap_remove: bpy.props.BoolProperty(
        name="Remove gaps",
        description="When trimming the sequences, remove gaps automatically",
        default=True,
    )

    TABLET_TRIM_DISTANCE_THRESHOLD = 6
    trim_start, channel_start = 0, 0
    trim_end, channel_end = 0, 0
    is_trimming = False

    mouse_start_y = -1.0

    draw_handler = None

    use_audio_scrub = False

    event_shift_released = True
    event_alt_released = True

    @classmethod
    def poll(cls, context):
        return context.sequences is not None

    def invoke(self, context, event):
        if context.screen.is_animation_playing:
            bpy.ops.screen.animation_cancel(restore_frame=False)

        self.use_audio_scrub = context.scene.use_audio_scrub
        context.scene.use_audio_scrub = False

        self.update_trim_end(context, event)
        self.trim_initialize(event)
        self.draw_start(context, event)

        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):

        if event.type in {"ESC"}:
            self.draw_stop()
            context.scene.use_audio_scrub = self.use_audio_scrub
            return {"CANCELLED"}

        # Start and end trim
        if event.type == "LEFTMOUSE" or (event.type in ["RET", "T"] and event.value == "PRESS"):
            self.trim_apply(context, event)
            self.draw_stop()

            # FIXME: Workaround Blender 2.80's audio bug, remove when fixed in Blender
            sequencer_workaround_2_80_audio_bug(context)

            context.scene.use_audio_scrub = self.use_audio_scrub
            return {"FINISHED"}

        # Update trim
        if event.type == "MOUSEMOVE":
            if self.mouse_start_y < 0.0:
                self.mouse_start_y = event.mouse_region_y

            self.draw_stop()
            self.update_trim_end(context, event)
            self.trim_end = context.scene.frame_current
            self.draw_start(context, event)
            return {"PASS_THROUGH"}

        return {"RUNNING_MODAL"}

    def trim_initialize(self, event):
        self.trim_start, self.channel_start = get_frame_and_channel(event)
        self.trim_end, self.channel_end = self.trim_start, self.channel_start
        self.is_trimming = True

    def trim_apply(self, context, event):
        start_x = context.region.view2d.region_to_view(
            x=event.mouse_region_x, y=event.mouse_region_y
        )[0]
        distance_to_start = abs(event.mouse_region_x - start_x)

        is_cutting = (
            self.trim_start == self.trim_end
            or event.is_tablet
            and distance_to_start <= self.TABLET_TRIM_DISTANCE_THRESHOLD
        )
        if is_cutting:
            self.cut(context)
        else:
            self.trim(context)
        self.is_trimming = False

    def update_trim_end(self, context, event):
        frame, self.channel_end = get_frame_and_channel(event)
        self.trim_end = find_snap_candidate(context, frame) if event.ctrl else frame
        context.scene.frame_current = self.trim_end

    def draw_start(self, context, event):
        """Initializes the drawing handler, see draw()"""
        to_select, to_delete = self.find_strips_to_trim(context)
        target_strips = to_select + to_delete

        draw_args = (
            self,
            context,
            self.trim_start,
            self.trim_end,
            self.mouse_start_y,
            target_strips,
            self.gap_remove,
        )
        self.draw_handler = bpy.types.SpaceSequenceEditor.draw_handler_add(
            draw, draw_args, "WINDOW", "POST_PIXEL"
        )

    def draw_stop(self):
        if self.draw_handler:
            bpy.types.SpaceSequenceEditor.draw_handler_remove(self.draw_handler, "WINDOW")

    def cut(self, context):
        to_select = self.find_strips_to_cut(context)
        bpy.ops.sequencer.select_all(action="DESELECT")
        for s in to_select:
            s.select = True

        frame_current = context.scene.frame_current
        context.scene.frame_current = self.trim_start
        bpy.ops.sequencer.cut(frame=context.scene.frame_current, type="SOFT", side="BOTH")
        context.scene.frame_current = frame_current

    def trim(self, context):
        to_select, to_delete = self.find_strips_to_trim(context)
        trim_strips(context, self.trim_start, self.trim_end, self.select_mode, to_select, to_delete)
        if self.gap_remove and self.select_mode == "CURSOR":
            context.scene.frame_current = min(self.trim_start, self.trim_end)
            bpy.ops.power_sequencer.gap_remove()
        else:
            context.scene.frame_current = self.trim_end

    def find_strips_to_cut(self, context):
        """
        Returns a list of strips to cut, either the strip hovered by the mouse or all strips under the
        time cursor, depending on the select_mode
        """
        to_cut = []
        overlapping_strips = []
        if self.select_mode == "CONTEXT":
            overlapping_strips = find_strips_mouse(
                context, self.trim_start, self.channel_start, self.select_linked
            )
            to_cut.extend(overlapping_strips)

        if self.select_mode == "CURSOR" or (
            not overlapping_strips and self.select_mode == "CONTEXT"
        ):
            for s in context.sequences:
                if s.lock:
                    continue
                if s.frame_final_start <= self.trim_start <= s.frame_final_end:
                    to_cut.append(s)
        return to_cut

    def cut_strips_or_gap(self, context, frame_cut):
        if self.cut_gaps and len(context.selected_sequences) == 0:
            bpy.ops.power_sequencer.gap_remove()
        else:
            frame_current = context.scene.frame_current
            context.scene.frame_current = frame_cut
            bpy.ops.sequencer.cut(frame=context.scene.frame_current, type="SOFT", side="BOTH")
            context.scene.frame_current = frame_current

    def find_strips_to_trim(self, context):
        """
        Returns two lists of strips to trim and strips to delete
        """
        to_trim, to_delete = [], []

        trim_start = min(self.trim_start, self.trim_end)
        trim_end = max(self.trim_start, self.trim_end)

        channel_min = min(self.channel_start, self.channel_end)
        channel_max = max(self.channel_start, self.channel_end)
        channels = set(range(channel_min, channel_max + 1))

        for s in context.sequences:
            if s.lock:
                continue
            if self.select_mode == "CONTEXT" and s.channel not in channels:
                continue

            if trim_start <= s.frame_final_start and trim_end >= s.frame_final_end:
                to_delete.append(s)
                continue
            if (
                s.frame_final_start <= trim_start <= s.frame_final_end
                or s.frame_final_start <= trim_end <= s.frame_final_end
            ):
                to_trim.append(s)

        return to_trim, to_delete


def draw(
    self, context, frame_start=-1, frame_end=-1, mouse_y=-1, target_strips=[], draw_arrows=False
):
    """
    Draws the line and arrows that represent the trim

    Params:
    - start and end are Vector(), the start and end of the drawn trim line's vertices in region coordinates
    """
    view_to_region = bpy.context.region.view2d.view_to_region

    # Detect and draw the gap's limits if not trimming any strips
    if not target_strips:
        strip_before, strip_after = find_closest_surrounding_cuts(context, frame_end)
        start = Vector((view_to_region(strip_before.frame_final_end, 1)[0], mouse_y))
        end = Vector((view_to_region(strip_after.frame_final_start, 1)[0], mouse_y))
        channels = [strip_before.channel, strip_after.channel]
    else:
        start = Vector((view_to_region(min(frame_start, frame_end), 1)[0], mouse_y))
        end = Vector((view_to_region(max(frame_start, frame_end), 1)[0], mouse_y))
        channels = set([s.channel for s in target_strips])

    y_min = view_to_region(0, math.floor(min(channels)))[1]
    y_max = view_to_region(0, math.floor(max(channels) + 1))[1]

    # Draw
    color_line = get_color_gizmo_primary(context)
    color_fill = color_line.copy()
    color_fill[-1] = 0.3

    bgl.glEnable(bgl.GL_BLEND)

    bgl.glLineWidth(3)
    draw_rectangle(
        SHADER, Vector((start.x, y_min)), Vector((end.x - start.x, abs(y_min - y_max))), color_fill
    )
    # Vertical lines
    draw_line(SHADER, Vector((start.x, y_min)), Vector((start.x, y_max)), color_line)
    draw_line(SHADER, Vector((end.x, y_min)), Vector((end.x, y_max)), color_line)

    offset = 20.0
    radius = 12.0
    if draw_arrows and end.x - start.x > 2 * offset + radius:
        center_y = (y_max + y_min) / 2.0
        center_1 = Vector((start.x + offset, center_y))
        center_2 = Vector((end.x - offset, center_y))
        draw_triangle_equilateral(SHADER, center_1, radius, color=color_line)
        draw_triangle_equilateral(SHADER, center_2, radius, math.pi, color=color_line)

    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)


def get_frame_and_channel(event):
    """
    Returns a tuple of (frame, channel)
    """
    frame_float, channel_float = bpy.context.region.view2d.region_to_view(
        x=event.mouse_region_x, y=event.mouse_region_y
    )
    return round(frame_float), math.floor(channel_float)
