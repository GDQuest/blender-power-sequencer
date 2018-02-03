import bpy


def get_current_hotkeys(group, space, region):
    """
    Collect all current Blender hotkeys in a group with matching space
    and region.

    Group names can be found in Blender > User Preferences > Input
    """
    hotkeys = []
    keyconfig_names = ['Blender', 'Blender Addon', 'Blender User']

    for kc_name in keyconfig_names:
        try:
            kc = bpy.context.window_manager.keyconfigs[kc_name]
            km = kc.keymaps[group]
            if km.space_type == space and km.region_type == region:
                hotkeys.extend(km.keymap_items)
        except KeyError:
            pass
    return hotkeys
