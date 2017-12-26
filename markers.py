import bpy
from bpy.props import EnumProperty, BoolProperty

# Regex to capture an ID within a string
ID_REGEX = r'-?([0-9]+)-?'

TITLE_PREFIX = r'TITLE'
NOTE_PREFIX = r''
TITLE_REGEX = r'^' + TITLE_PREFIX + ID_REGEX
NOTE_REGEX = r'^' + NOTE_PREFIX + ID_REGEX


class SyncTitles(bpy.types.Operator):
    bl_idname = 'power_sequencer.synchronize_titles'
    bl_label = 'PS.Synchronize titles'
    bl_description = 'Snap the selected image or text strips to the \
                      corresponding title marker. The marker and strip names \
                      have to start with TITLE-001, ...'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        markers = bpy.context.scene.timeline_markers
        selection = bpy.context.selected_sequences

        if not markers and selection:
            if not markers:
                self.report({"INFO"}, "No markers, operation cancelled.")
            else:
                self.report({"INFO"}, "No sequences selected, operation cancelled.")
            return {"CANCELLED"}

        title_markers = find_markers(TITLE_REGEX)
        if not title_markers:
            self.report({"INFO"}, "No title markers found, operation cancelled.")

        matched = match_sequences_and_markers(selection, title_markers, TITLE_REGEX)
        for s, m in matched:
            s.frame_start = m.frame
        return {'FINISHED'}


def match_sequences_and_markers(sequences, markers, regex):
    """Takes a list of sequences, of markers, and checks if they both
        match a regular expression.
        Returns a list of pairs of sequence and marker as tuples

        Args:
        - sequences, the list of sequences
        - markers, a list of markers
        - regex, the regular expression to match"""
    if not sequences and markers and regex:
        raise AttributeError('missing attributes')

    import re
    from .functions.global_settings import SequenceTypes
    sequences = (s for s in sequences if s.type not in SequenceTypes.EFFECT)

    return_list = []
    re_title = re.compile(regex)
    for s in sequences:
        found = re_title.match(s.name)
        title_id = int(found.group(1)) if found else None
        for m in markers:
            found = re_title.match(m.name)
            marker_id = int(found.group(1)) if found else None
            if marker_id == title_id:
                return_list.append((s, m))
                break
    return return_list


class AddTitleMarker(bpy.types.Operator):
    bl_idname = 'power_sequencer.add_title_marker'
    bl_label = 'PS.Add title marker'
    bl_description = 'Add a title marker to quickly sync TITLE strips'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.marker.add()
        marker_name = create_marker_name(prefix=TITLE_PREFIX,
                                         name="",
                                         title_marker=True)
        bpy.ops.marker.rename(name=marker_name)
        return {'FINISHED'}


class AddNumberedMarker(bpy.types.Operator):
    bl_idname = 'power_sequencer.add_numbered_marker'
    bl_label = 'PS.Add numbered marker'
    bl_description = 'Add a numbered marker to quickly sync image'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.marker.add()
        marker_name = create_marker_name(prefix=NOTE_PREFIX,
                                         name="",
                                         title_marker=False)
        bpy.ops.marker.rename(name=marker_name)
        return {'FINISHED'}


def create_marker_name(title_marker=False, prefix="", name="", use_id=True):
    """Create and return a string with a prefix, ID, and name
    Args:
        - title_marker: required, optional flag"""

    markers = bpy.context.scene.timeline_markers
    regex = TITLE_REGEX if title_marker else NOTE_REGEX

    ids = []
    for m in markers:
        found_id = string_find_id(m.name, regex)
        if found_id:
            ids.append(found_id)
    new_id = max(ids) + 1 if ids else 1
    name = prefix + '{0:03d}'.format(new_id) + name
    return name


def find_markers(regex):
    """Finds and returns all markers using REGEX
    Args:
        - regex, the re match pattern to use"""
    if not regex:
        raise AttributeError('regex parameter missing')

    import re
    regex = re.compile(regex)
    markers = bpy.context.scene.timeline_markers
    markers = (m for m in markers if regex.match(m.name))
    return markers


def string_find_id(string, regex):
    """Find a marker's ID using a regular expression
    returns the ID as int if found, otherwise returns None
    Args:
        -string, any string
        -regex, the regex pattern to match."""

    if not string and regex:
        raise AttributeError("Missing name or regex attribute")

    import re
    index = re.search(regex, string)
    if index:
        found_id = index.group(1)
        return int(found_id) if found_id else None
    return None


class SnapMarkerToCursor(bpy.types.Operator):
    bl_idname = 'power_sequencer.snap_marker_to_cursor'
    bl_label = 'PS.Snap marker to cursor'
    bl_description = 'Snap the selected marker to the time cursor'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        markers = bpy.context.scene.timeline_markers

        selected_markers = []
        for marker in markers:
            if marker.select:
                selected_markers.append(marker)

        if not selected_markers:
            return {'CANCELLED'}
        if len(selected_markers) > 1:
            self.report(
                {"ERROR_INVALID_INPUT"},
                "You can only snap 1 marker at a time. Operation cancelled.")
            return {'CANCELLED'}

        selected_markers[0].frame = bpy.context.scene.frame_current
        return {'FINISHED'}


class GoToNextMarker(bpy.types.Operator):
    """Moves the time cursor to the next marker"""
    bl_idname = "power_sequencer.go_to_marker"
    bl_label = "PS.Go to marker"
    bl_options = {'REGISTER', 'UNDO'}

    target_marker = EnumProperty(
        items=[
            ('left', 'left', 'left'), ('right', 'right', 'right')
        ],
        name='Target marker',
        description=
        'Move to the closest marker to the left or to the right of the cursor',
        default='left')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if not bpy.context.scene.timeline_markers:
            self.report({"ERROR_INVALID_INPUT"},
                        "There are no markers. Operation cancelled.")
            return {"CANCELLED"}

        frame = bpy.context.scene.frame_current
        previous_marker, next_marker = find_neighbor_markers(frame)

        if not previous_marker and self.target_marker == 'left' or not next_marker and self.target_marker == 'right':
            self.report({"INFO"}, "No more markers to jump to on the %s side."
                        % self.target_marker)
            return {"CANCELLED"}

        previous_time = previous_marker.frame if previous_marker else None
        next_time = next_marker.frame if next_marker else None

        bpy.context.scene.frame_current = previous_time if self.target_marker == 'left' or not next_time else next_time
        return {'FINISHED'}


class DeleteClosestMarker(bpy.types.Operator):
    bl_idname = 'power_sequencer.delete_closest_marker'
    bl_label = 'PS.Delete closest marker'
    bl_description = 'Delete the marker closest to the mouse'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        markers = bpy.context.scene.timeline_markers
        if not markers:
            return {"CANCELLED"}

        frame = bpy.context.scene.frame_current
        for m in markers:
            if m.frame == frame:
                markers.remove(m)
                return {'FINISHED'}

        previous_marker, next_marker = find_neighbor_markers(frame)

        marker = next_marker if next_marker else previous_marker
        if next_marker and previous_marker:
            if abs(frame - next_marker.frame) <= abs(frame -
                                                     previous_marker.frame):
                marker = next_marker
            else:
                marker = previous_marker
        markers.remove(marker)
        return {'FINISHED'}


class SetPreviewBetweenMarkers(bpy.types.Operator):
    bl_idname = 'power_sequencer.set_preview_between_markers'
    bl_label = 'PS.Set preview between closest markers'
    bl_description = "Set the timeline's preview range using the 2 markers closest to the time cursor"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        if not bpy.context.scene.timeline_markers:
            self.report({"ERROR_INVALID_INPUT"},
                        "There are no markers. Operation cancelled.")
            return {"CANCELLED"}

        frame = bpy.context.scene.frame_current
        previous_marker, next_marker = find_neighbor_markers(frame)

        if not (previous_marker and next_marker):
            self.report({"ERROR_INVALID_INPUT"},
                        "There are no markers. Operation cancelled.")
            return {"CANCELLED"}

        frame_start = previous_marker.frame if previous_marker else 0
        if next_marker:
            frame_end = next_marker.frame
        else:
            from operator import attrgetter
            frame_end = max(bpy.context.scene.sequence_editor.sequences,
                            key=attrgetter('frame_final_end')).frame_final_end

        from .functions.sequences import set_preview_range
        set_preview_range(frame_start, frame_end)
        return {'FINISHED'}


def find_neighbor_markers(frame=None):
    """Returns a tuple containing the closest marker to the left and to the right of the frame"""
    markers = bpy.context.scene.timeline_markers

    if not (frame and markers):
        return None, None

    from operator import attrgetter
    markers = sorted(markers, key=attrgetter('frame'))

    previous_marker, next_marker = None, None
    for m in markers:
        previous_marker = m if m.frame < frame else previous_marker
        if m.frame > frame:
            next_marker = m
            break

    return previous_marker, next_marker
