import bpy
from math import floor
import bgl
from mathutils import Vector

from bpy.props import BoolProperty, IntProperty, EnumProperty
from .utils.find_strips_mouse import find_strips_mouse
from .utils.trim_strips import trim_strips


class MouseCut(bpy.types.Operator):
    """Cut, trim and remove gaps with mouse clicks"""
    bl_idname = "power_sequencer.mouse_cut"
    bl_label = "Mouse Cut"
    bl_description = "Fast strip cutting based on mouse position"
    bl_options = {'REGISTER', 'UNDO'}

    select_mode = EnumProperty(
        items=[('mouse', 'Mouse',
                'Only select the strip hovered by the mouse'),
               ('cursor', 'Time cursor',
                'Select all of the strips the time cursor overlaps'),
               ('smart', 'Smart',
                'Uses the selection if possible, else uses the other modes')],
        name="Selection mode",
        description="Cut only the strip under the mouse or all strips under the time cursor",
        default='smart')
    select_linked = BoolProperty(
        name="Use linked time",
        description="In mouse or smart mode, always cut linked strips if this is checked",
        default=False)
    remove_gaps = BoolProperty(
        name="Remove gaps",
        description="When trimming the sequences, remove gaps automatically",
        default=True)
    cut_gaps = BoolProperty(
        name="Cut gaps",
        description="If you click on a gap, remove it",
        default=True)

    auto_move_cursor = BoolProperty(
        name="Auto move cursor",
        description="When trimming the sequence, auto move the cursor if playback is active",
        default=True)
    cursor_offset = IntProperty(
        name="Cursor trim offset",
        description="On trim, during playback, offset the cursor to better see if the cut works",
        default=12,
        min=0)
    threshold_trim_distance = IntProperty(
        name="Tablet trim distance",
        description="If you use a pen tablet, the trim will only happen past this distance",
        default=6,
        min=0)

    use_pen_tablet = False
    mouse_start_x, mouse_start_y = 0.0, 0.0

    frame_start, start_channel = 0, 0
    frame_end, end_channel = 0, 0
    select_mouse, action_mouse = '', ''
    cut_mode = ''
    
    mouse_vec_start = Vector([0, 0])
    handle_cut_trim_line = None
    
    function = bpy.props.StringProperty("")

    @classmethod
    def poll(cls, context):
        return context.sequences is not None

    def invoke(self, context, event):
        # Detect pen tablets
        if event.pressure not in [0.0, 1.0]:
            self.use_pen_tablet = True
            self.mouse_start_x, self.mouse_start_y = event.mouse_region_x, event.mouse_region_y

        frame_float, channel_float = context.region.view2d.region_to_view(
            x=event.mouse_region_x, y=event.mouse_region_y)
        self.frame_start, self.start_channel = round(frame_float), floor(channel_float)
        self.frame_end = self.frame_start

        # Reverse keymaps if the user selects with the left mouse button
        self.select_mouse = 'RIGHTMOUSE'
        self.action_mouse = 'LEFTMOUSE'
        if bpy.context.user_preferences.inputs.select_mouse == 'LEFT':
            self.select_mouse = 'LEFTMOUSE'
            self.action_mouse = 'RIGHTMOUSE'
        
        self.mouse_vec_start = Vector([event.mouse_region_x, event.mouse_region_y])

        bpy.context.scene.frame_current = self.frame_start
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        # if event.type in {'LEFTMOUSE', 'RIGHTMOUSE'}:
        #     print('type: {!s}, value: {!s}'.format(event.type, event.value))
        if event.type in {'ESC'}:
            return {'CANCELLED'}

        elif event.type == self.action_mouse and event.value == 'RELEASE':
            
            if self.handle_cut_trim_line:
                bpy.types.SpaceSequenceEditor.draw_handler_remove(self.handle_cut_trim_line, 'WINDOW')
            
            self.select_mode = 'cursor' if event.shift else 'smart'

            cursor_distance = abs(event.mouse_region_x - self.mouse_start_x)
            if (self.use_pen_tablet and cursor_distance <= self.threshold_trim_distance) \
               or self.frame_start == self.frame_end:
                to_select = self.find_strips_to_cut()
                bpy.ops.sequencer.select_all(action='DESELECT')
                for s in to_select:
                    s.select = True
                print(bpy.context.selected_sequences)
                self.cut_strips_or_gap(self.frame_start)
            else:
                to_select, to_delete = self.find_strips_to_trim()
                trim_strips(self.frame_start, self.frame_end, self.select_mode,
                            to_select, to_delete)

                if self.remove_gaps and self.select_mode == 'cursor':
                    bpy.context.scene.frame_current = min(self.frame_start, self.frame_end)
                    bpy.ops.sequencer.gap_remove()
                else:
                    bpy.context.scene.frame_current = self.frame_end
            return {'FINISHED'}

        elif event.type == 'MOUSEMOVE':
            x, y = context.region.view2d.region_to_view(
                x=event.mouse_region_x, y=event.mouse_region_y)
            
            if self.handle_cut_trim_line:
                bpy.types.SpaceSequenceEditor.draw_handler_remove(self.handle_cut_trim_line, 'WINDOW')
            
            args = (self, 
                    Vector([self.mouse_vec_start.x, self.mouse_vec_start.y]), 
                    Vector([round(event.mouse_region_x), self.mouse_vec_start.y]),
                    event.shift)
            self.handle_cut_trim_line = bpy.types.SpaceSequenceEditor.draw_handler_add(
                    draw_cut_trim, args, 'WINDOW', 'POST_PIXEL')
            
            self.frame_end, self.end_channel = round(x), floor(y)
            bpy.context.scene.frame_current = self.frame_end
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def find_strips_to_cut(self):
        """
        Finds and Returns a list of strips to cut
        """
        to_select = []
        overlapping_strips = []
        if self.select_mode == 'smart':
            overlapping_strips = find_strips_mouse(
                self.frame_start, self.start_channel, self.select_linked)
            to_select.extend(overlapping_strips)

        if self.select_mode == 'cursor' or (not overlapping_strips and
                                            self.select_mode == 'smart'):
            for s in bpy.context.sequences:
                if s.lock:
                    continue
                if s.frame_final_start <= self.frame_start <= s.frame_final_end:
                    to_select.append(s)
        return to_select

    def cut_strips_or_gap(self, frame_cut):
        if self.cut_gaps and len(bpy.context.selected_sequences) == 0:
            bpy.ops.sequencer.gap_remove(all=False)
        else:
            frame_current = bpy.context.scene.frame_current
            bpy.context.scene.frame_current = frame_cut
            bpy.ops.sequencer.cut(
                frame=bpy.context.scene.frame_current,
                type='SOFT',
                side='BOTH')
            bpy.context.scene.frame_current = frame_current

    def find_strips_to_trim(self):
        """
        Finds and Returns two lists of strips to trim and strips to delete
        """
        to_select, to_delete = [], []
        overlapping_strips = []
        trim_start, trim_end = min(self.frame_start, self.frame_end), max(
            self.frame_start, self.frame_end)
        if self.select_mode == 'smart':
            overlapping_strips = find_strips_mouse(
                trim_start, self.start_channel, self.select_linked)
            to_select.extend(overlapping_strips)

        if self.select_mode == 'cursor' or (not overlapping_strips and
                                            self.select_mode == 'smart'):
            for s in bpy.context.sequences:
                if s.lock:
                    continue

                if trim_start <= s.frame_final_start and trim_end >= s.frame_final_end:
                    to_delete.append(s)
                    continue
                if s.frame_final_start <= trim_start <= s.frame_final_end or \
                   s.frame_final_start <= trim_end <= s.frame_final_end:
                    to_select.append(s)
        return to_select, to_delete


def draw_cut_trim(self, start, end, will_remove_gap):
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(2)
    bgl.glPushMatrix()
    
    bgl.glColor4f(1.0, 0.0, 1.0, 0.5)
    
    # The Horizontal Line
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex2f(start.x, start.y)
    bgl.glVertex2f(end.x, end.y)
    bgl.glEnd()
    
    # The Start Vertical Line
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex2f(start.x, start.y)
    bgl.glVertex2f(start.x, 0)
    bgl.glEnd()
    
    # The End Vertical Line
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex2f(end.x, end.y)
    bgl.glVertex2f(end.x, 0)
    bgl.glEnd()
    
    if will_remove_gap:
        # First Arrow Head
        bgl.glBegin(bgl.GL_LINES)
        bgl.glVertex2f(start.x + ((end.x - start.x) * 0.25), start.y)
        bgl.glVertex2f(start.x + ((end.x - start.x) * 0.25) - 10, start.y + 10)
        bgl.glEnd()
        
        bgl.glBegin(bgl.GL_LINES)
        bgl.glVertex2f(start.x + ((end.x - start.x) * 0.25), start.y)
        bgl.glVertex2f(start.x + ((end.x - start.x) * 0.25) - 10, start.y - 10)
        bgl.glEnd()
        
        # Last Arrow Head
        bgl.glBegin(bgl.GL_LINES)
        bgl.glVertex2f(end.x - ((end.x - start.x) * 0.25), end.y)
        bgl.glVertex2f(end.x - ((end.x - start.x) * 0.25) + 10, end.y + 10)
        bgl.glEnd()
        
        bgl.glBegin(bgl.GL_LINES)
        bgl.glVertex2f(end.x - ((end.x - start.x) * 0.25), end.y)
        bgl.glVertex2f(end.x - ((end.x - start.x) * 0.25) + 10, end.y - 10)
        bgl.glEnd()
    
    bgl.glPopMatrix()
    
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
