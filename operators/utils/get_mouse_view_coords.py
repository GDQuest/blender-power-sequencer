from math import floor


def get_mouse_frame_and_channel(context, event):
    """
    Convert mouse coordinates from the event, from
    pixels to frame, channel.
    Returns a tuple of frame, channel as integers
    """
    view2d = context.region.view2d
    frame, channel = view2d.region_to_view(
        event.mouse_region_x,
        event.mouse_region_y)
    return round(frame), floor(channel)

