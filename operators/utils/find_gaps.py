# sort bpy.context.sequences by frame_final_start, frame_final_end
# loop over and find the first or all gaps in the frame range
# subtract the gap's size from the frame_start of all strips after the gap(s), reusing the sorted sequences list

import bpy
from operator import attrgetter

def find_gaps(sequences):
    sorted_sequences = sorted(sequences, key=attrgetter('frame_final_start', 'frame_final_end'))
    # Detect disconnected sequence blocks, starting from first frame in the sequencer
