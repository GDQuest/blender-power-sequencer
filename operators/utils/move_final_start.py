import bpy

def move_final_start(strip, frame):
    """
    Moves a strip based on its frame_final_start without changing its 
    duration.
    Args:
    - strip: The strip to be moved.
    - frame: The frame, the frame_final_start of the strip will be placed at.
    """
    strip.frame_start = frame + strip.frame_start - strip.frame_final_start