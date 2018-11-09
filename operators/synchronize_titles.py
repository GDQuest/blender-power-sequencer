import bpy

from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


# TODO: rewrite to sync strips to corresponding identifiers instead
# See https://github.com/GDquest/Blender-power-sequencer/issues/55
class SynchronizeTitles(bpy.types.Operator):
    """
    *brief* Snap the selected image or text strips to the corresponding title marker


    The marker and strip names have to start with TITLE-001
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    TITLE_REGEX = r'^TITLE-?([0-9]+)-?'

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
                self.report({"INFO"},
                            "No sequences selected, operation cancelled.")
            return {"CANCELLED"}

        title_markers = self.find_markers(self.TITLE_REGEX)
        if not title_markers:
            self.report({"INFO"},
                        "No title markers found, operation cancelled.")

        matched = self.match_sequences_and_markers(selection, title_markers, self.TITLE_REGEX)
        for s, m in matched:
            s.frame_start = m.frame
        return {'FINISHED'}

    def match_sequences_and_markers(self, sequences, markers, regex):
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
        from .utils.global_settings import SequenceTypes
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

    def find_markers(self, regex):
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

