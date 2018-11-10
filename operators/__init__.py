from .add_speed import AddSpeed
from .add_transform import AddTransform
from .align_audios import AlignAudios
from .border_select import BorderSelect
from .change_playback_speed import ChangePlaybackSpeed
from .channel_offset import ChannelOffset
from .concatenate_strips import ConcatenateStrips
from .copy_selected_sequences import CopySelectedSequences
from .crossfade_add import CrossfadeAdd
from .crossfade_edit import CrossfadeEdit
from .crossfade_remove import CrossfadeRemove
from .cut_strips_under_cursor import CutStripsUnderCursor
from .decrease_playback_speed import DecreasePlaybackSpeed
from .delete_direct import DeleteDirect
from .deselect_all_left_or_right import DeselectAllStripsLeftOrRight
from .deselect_handles_and_grab import DeselectHandlesAndGrab
from .duplicate_move import DuplicateMove
from .fade_add import FadeAdd
from .fade_clear import FadeClear
from .grab_closest_handle_or_cut import GrabClosestCut
from .grab import Grab
from .grab_sequence_handles import GrabSequenceHandles
from .import_local_footage import ImportLocalFootage
from .increase_playback_speed import IncreasePlaybackSpeed
from .jump_time_offset import JumpTimeOffset
from .jump_to_cut import JumpToCut
from .make_still_image import MakeStillImage
from .marker_delete_closest import MarkerDeleteClosest
from .marker_delete_direct import MarkerDeleteDirect
from .marker_go_to_next import MarkerGoToNext
from .markers_as_timecodes import CopyMarkersAsTimecodes
from .markers_create_from_selected import MarkersCreateFromSelectedStrips
from .marker_snap_to_cursor import MarkerSnapToCursor
from .markers_snap_matching_strips import MarkersSnapMatchingStrips
from .meta_resize_to_content import MetaResizeToContent
from .meta_separate import MetaSeparateAndTrim
from .meta_trim_content_to_bounds import MetaTrimContentToBounds
from .mouse_cut import MouseCut
from .mouse_space_strips import MouseSpaceStrips
from .mouse_toggle_mute import MouseToggleMute
from .mouse_trim import MouseTrim
from .open_project_directory import OpenProjectDirectory
from .preview_closest_cut import PreviewClosestCut
from .preview_to_selection import PreviewToSelection
from .remove_gaps import RemoveGaps
from .render_for_web import RenderForWeb
from .ripple_delete import RippleDelete
from .save_direct import SaveDirect
from .scene_create_from_selection import SceneCreateFromSelection
from .scene_cycle import SceneCycle
from .select_closest_to_mouse import SelectClosestToMouse
from .select_linked_effect import SelectLinkedEffect
from .select_related_strips import SelectRelatedStrips
from .select_strips_under_cursor import SelectStripsUnderCursor
from .set_preview_between_markers import SetPreviewBetweenMarkers
from .set_timeline_range import SetTimelineRange
from .smart_snap import SmartSnap
from .snap_selection_to_cursor import SnapSelectionToCursor
from .speed_remove_effect import Unspeed
from .swap_strips import SwapStrips
from .synchronize_titles import SynchronizeTitles
from .toggle_selected_mute import ToggleSelectedMute
from .toggle_waveforms import ToggleWaveforms
from .trim_three_point_edit import TrimThreePointEdit
from .trim_to_surrounding_cuts import TrimToSurroundingCuts
from .export_sequence import ExportSequence
from .go_to_in_out_selection import GoToInOut
from .move_selected_strip import MoveSelectedClips
from .select_by_channel import SelectByChannel
from .select_handles import SelectHandles
from .select_left_right_from_active import SelectLeftRight
from .select_playing import SelectPlaying
from .set_scene_settings import SetSceneScene

doc = {
    'sequencer.refresh_all': {
        'name': 'Refresh All',
        'description': '',
        'shortcuts': [
            ({'type': 'R', 'value': 'PRESS', 'shift': True}, {}, 'Refresh All')
        ],
        'demo': '',
        'keymap': 'Sequencer'
    }
}

