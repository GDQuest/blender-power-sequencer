import bpy
from move_final_start import move_final_start

def swap_strips(strip_1, strip_2):
    """
    Swaps 2 strips between them. More specific, places the first strip in the
    channel and starting frame (frame_final_start) of the second strip, and
    places the second strip in the channel and starting frame (frame_final_end)
    of the first strip. If the biggest in duration strip doesn't fit in the 
    space of the smallest strip, it does nothing.
    Args:
    - strip_1: The first strip to be swapped.
    - strip_2: The second strip to be swapped.
    Returns True if the strips have been swapped, otherwise False.
    """
    
    #Finds the smallest and biggest strip out of strip_1 and strip_2
    if strip_1.frame_final_duration > strip_2.frame_final_duration:
        big_strip = strip_1
        small_strip = strip_2
    else:
        big_strip = strip_2
        small_strip = strip_1
    
    #Special case of when the small_strip is placed at the left of the big_strip
    #and they are in the same channel
    if small_strip.frame_final_start < big_strip.frame_final_start and \
            small_strip.channel == big_strip.channel:
        #Checks if the swap would make the small_strip to limit the space of the
        #big_strip
        if big_strip.frame_final_start < small_strip.frame_final_start + \
                    big_strip.frame_final_duration:
            return False
    
    #All the strips
    sequences = bpy.context.sequences
    #The channel of small_strip
    small_strip_channel = small_strip.channel
    
    #Checks if the 2 strips don't have the same duration
    if small_strip.frame_final_duration != big_strip.frame_final_duration:
        #Passes throught all the strips, to find if the bigger strip fits in the
        #space of the smaller
        for strip in sequences:
            #Ignores the small_strip and big_strip
            if strip == small_strip or strip == big_strip:
                continue
            
            #Ignores the strips with a different channel than the small_strip,
            #as they can't interfere with the space needed for the big_strip
            if strip.channel != small_strip_channel:
                continue
            
            #Ignores all the strips at the left of small_strip, as they can't
            #interfere with the space needed for the big_strip
            if strip.frame_final_end < small_strip.frame_final_start:
                continue
            
            #Checks if the current strip would interfere with the big_strip if
            #the big_strip was placed in the space of the small_strip
            if strip.frame_final_start < small_strip.frame_final_start + \
                    big_strip.frame_final_duration:
                return False
    
    #The strips can be swapped
       
    #The frame_final_end of the last strip (the strip with frame_final_end >= of 
    #every other strip)
    end_frame = 0
    #Finds the end_frame      
    for strip in sequences:
        if end_frame < strip.frame_final_end:
            end_frame = strip.frame_final_end   
    
    #Stores the information of the location of the 2 strips
    big_strip_start = big_strip.frame_final_start
    big_strip_channel = big_strip.channel
    small_strip_start = small_strip.frame_final_start
    small_strip_channel = small_strip.channel
    
    #Places the small_strip in a temporary location, guaranteed to leave empty
    #its previous location
    move_final_start(small_strip, end_frame)
    #Moves the small_strip in the target channel
    small_strip.channel = big_strip_channel
    
    #Places the big_strip in the initial location of the small_strip.
    #Temporary places the big_strip at the right of the small_strip
    move_final_start(big_strip, end_frame + small_strip.frame_final_duration)
    #Moves the big_strip in the target channel
    big_strip.channel = small_strip_channel
    #Places the big_strip in its target location
    move_final_start(big_strip, small_strip_start)
    
    #Places the small_strip in its target location
    move_final_start(small_strip, big_strip_start)
    
    return True