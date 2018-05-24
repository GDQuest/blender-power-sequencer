import math
from markdown2 import markdown


def make_toc_label(label, description):
    """
    Make a table-of-contents item with a link to the operator and
    description for it's tooltip.
    """
    description = reflow_paragraph(description, 31)

    hla = label.replace(' ', '_')
    html_link = ''.join([
        '<a name="top_', hla, '" href="#', hla, '" title="' + description + '">',
        label, '</a>'])
    return html_link


def reflow_paragraph(text, space, leading_space=''):
    '''
    Reflow a flattened paragraph so it fits inside horizontal
    space
    '''
    words = text.split(' ')
    growing_string = leading_space
    output_list = []

    while len(words) > 0:
        if growing_string == leading_space:
            growing_string += words[0]
            words.pop(0)
        elif len(growing_string + ' ' + words[0]) <= space:
            growing_string += ' ' + words[0]
            words.pop(0)
        else:
            output_list.append(growing_string + '\n')
            growing_string = leading_space
    output_list.append(growing_string)
    return ''.join(output_list)


def make_toc(info):
    """
    Generate a table of contents from the operator info
    """
    toc = ['<table>']

    labels = []

    for key in sorted(info.keys()):
        label = info[key]['name']
        description = info[key]['description']
        labels.append(make_toc_label(label, description))

    columns = [[], [], [], []]
    row_count = math.ceil(len(labels) / len(columns))

    i = 0
    col = 0
    while i < len(labels):
        for x in range(row_count):
            try:
                columns[col].append(labels[i])
                i += 1
            except IndexError:
                break
        col += 1

    dead_column = False
    column_width = str(int((1 / len(columns)) * 888)) + 'px'
    for row in range(row_count):
        toc.append('    <tr>')

        for col in range(len(columns)):
            try:
                toc.append('        <td width=' + column_width + '>' + columns[col][row] + '</td>')
            except IndexError:
                if dead_column == False:
                    remaining_rows = row_count - row
                    toc.append('        <td width=' + column_width + ' rowspan="' + str(remaining_rows) + '"></td>')
                    dead_column = True
        toc.append('    </tr>')
    toc.append('</table>')

    return '\n'.join(toc)


def make_seg_label(label):
    """
    Make the title label for an operator segment with a link back to the
    matching table of contents label
    """
    hla = label.replace(' ', '_')
    seg_label = ''.join([
        '    ', '<h3>', '<a name="', hla, '" href="#top_', hla, '">',
        label, '</a>', '</h3>'])
    return seg_label


def make_shortcuts_table(op_dict):
    """
    Make a table showing all the keyboard shortcuts, their functions,
    and a demo for a given operator
    """
    shortcuts = []
    functions = []
    demo = op_dict['demo']

    for i in range(len(op_dict['shortcuts'])):
        shortcuts.append(op_dict['shortcuts'][i].split(';')[0].strip())
        functions.append(op_dict['shortcuts'][i].split(';')[1].strip())

    for i in range(len(shortcuts)):
        hotkeys = shortcuts[i].split(' ')
        for x in range(len(hotkeys)):
            hotkeys[x] = '<img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/' + hotkeys[x].strip().upper() + '.png" alt="' + hotkeys[x].strip().upper() + '">'
        shortcuts[i] = ''.join(hotkeys)

    hotkeys_width = str(int((888 - 256) * 0.33)) + 'px'
    function_width = str(int((888 - 256) * 0.66)) + 'px'
    table = ['<table>']
    table.append('    <tr>')
    table.append('        <th width=' + hotkeys_width + '>Shortcut</th>')

    if len(functions) > 0:
        table.append('        <th width=' + function_width + '>Function</th>')
    if demo != '':
        table.append('        <th width=256px>Demo</th>')

    for i in range(len(shortcuts)):
        table.append('    <tr>')

        table.append('        <td align="center">' + ''.join(shortcuts[i]) + '</td>')
        table.append('        <td>' + markdown(functions[i]) + '</td>')

        if i == 0 and demo != '':
            table.append('        <td align="center" rowspan="' + str(len(shortcuts)) + '">' + '<img src="' + demo + '"></td>')

        table.append('    </tr>')
    table.append('</table>')
    return '\n'.join(table)


def make_operator_segments(info):
    """
    Using the operator info, make segments that put all that info together.
    """
    segments = []

    for key in sorted(info.keys()):
        label = make_seg_label(info[key]['name'])
        description = markdown(info[key]['description'])
        shortcut_table = make_shortcuts_table(info[key])

        segments.append('\n'.join([label, description, shortcut_table]))
    return '\n'.join(segments)


def make_readme():
    """
    Generate a nice-looking readme.
    """

    readme_path = 'README.rst'

    title = """
<h1 align="center">
  Blender Power Sequencer</br>
  <small>The Free add-on for content creators</small>
</h1>

<p align='center'>
  <img src="https://i.imgur.com/6tVdzBQ.jpg" alt="Power Sequencer logo, with the add-on's name and strips cut in two" />
</p>
"""

    intro = markdown("""
I've made [hundreds of tutorials](http://youtube.com/c/gdquest) over the
years. After working with popular professional programs like Vegas and
Resolve, I now **work exclusively with Blender**. It does have some
limitations, but it's the most stable and versatile tool you'll find out
there.

I built Power Sequencer to help us edit videos as fast as possible. The
add-on is getting better month after month, and it's yours for Free.

## Contributing ##

This add-on is a living, open project, and we'd be glad to welcome new
contributors! We need people to:

- Code new features
- Improve existing features
- Help solidify the code
- Write mini-tutorials on the [docs repository](https://github.com/GDquest/Blender-power-sequencer-docs/)

## Installation ##

1. Download the repository. Go to
   [Releases](https://github.com/GDquest/Blender-power-sequencer/releases)
   for a stable version, or click the green button above to get the most
   recent (and potentially unstable) version.
2. Open Blender
3. Go to File > User Preferences > Addons
4. Click "Install From File" and navigate to the downloaded .zip file
   and install
5. Check the box next to "VSE: Power Sequencer"
6. Save User Settings so the addon remains active every time you open
   Blender

## Usage ##
The docs are in progress. Until the dedicated website is ready, you can
find them on the [power-sequencer-docs repository](https://github.com/GDquest/Blender-power-sequencer-docs/).
There's also a growing list of [Free video tutorials](https://www.youtube.com/playlist?list=PLhqJJNjsQ7KFjp88Cu57Zb9_wFt7nlkEI)
on Youtube (*14 videos at the time of writing*).

## Other add-ons

Here are other recommended add-ons for a better editing workflow:

Daniel Oakey's [rewrite of VSE Transform Tools](https://github.com/doakey3/VSE_Transform_Tools).
This tool lets you animate and move strips from the video preview. The
original add-on was abandoned a few years ago. Daniel fixed and rewrote
it so now it's super slick!

## Credits

- [davcri](https://github.com/davcri)
- [Daniel Oakey](https://github.com/doakey3)
- [ Nathan Lovato ](https://twitter.com/NathanGDquest)
""".strip(), extras=['cuddled_lists'])

    operator_info = {
        'power_sequencer.add_crossfade': {
            'name': 'Add Crossfade',
            'description': "Based on the active strip, finds the closest next sequence of a similar type, moves it so it overlaps the active strip, and adds a gamma cross effect between them. Works with MOVIE, IMAGE and META strips",
            'shortcuts': ['Ctrl Alt C; Add Crossfade'],
            'demo': 'https://i.imgur.com/ZyEd0jD.gif',
        },
        'power_sequencer.add_speed': {
            'name': 'Add Speed',
            'description': "Add 2x speed to strip and set it's frame end accordingly. Wraps both the strip and the speed modifier into a META strip.",
            'shortcuts': ['Shift PLUS; Add Speed'],
            'demo': 'https://i.imgur.com/lheIZzA.gif',
        },
        'power_sequencer.add_transform': {
            'name': 'Add Transform',
            'description': "For each strip in the selection:\n\n* Filters the selection down to image and movie strips\n* Centers the pivot point of image strips\n* Adds a transform effect and sets it to ALPHA_OVER",
            'shortcuts': ['T; Add Transform'],
            'demo': '',
        },
        'power_sequencer.border_select': {
            'name': 'Border Select',
            'description': "",
            'shortcuts': ['Shift B; Border Select'],
            'demo': '',
        },
        'power_sequencer.change_playback_speed': {
            'name': 'Change Playback Speed',
            'description': 'Change the playback_speed property using an operator property. Used with keymaps',
            'shortcuts': ['ONE; Speed to 1x', 'TWO; Speed to 1.33x', 'THREE; Speed to 1.66x', 'FOUR; Speed to 2x'],
            'demo': '',
        },
        'power_sequencer.channel_offset': {
            'name': 'Channel Offset',
            'description': 'Move selected strip to the nearest open channel above/down',
            'shortcuts': ['Alt UP_ARROW; Move to open channel above', 'Alt DOWN_ARROW; Move to open channel above'],
            'demo': '',
        },
        'power_sequencer.clear_fades': {
            'name': 'Clear Fades',
            'description': 'Set strip opacity to 1.0 and remove all opacity-keyframes',
            'shortcuts': ['Ctrl Alt F; Clear fades'],
            'demo': '',
        },
        'power_sequencer.concatenate_strips': {
            'name': 'Concatenate Strips',
            'description': 'Concatenates selected strips in a channel (removes the gap between them) If a single strip is selected, either the next strip in the channel will be concatenated, or all strips in the channel will be concatenated depending on which shortcut is used.',
            'shortcuts': ['C; Concatenate selected strips in channel, or concatenate & select next strip in channel if only 1 strip selected', 'Shift C;Concatenate selected strips in channel, or concatenate all strips in channel if only 1 strip selected'],
            'demo': 'https://i.imgur.com/YyEL8YP.gif',
        },
        'power_sequencer.copy_selected_sequences': {
            'name': 'Copy Selected Sequences',
            'description': 'Copies the selected sequences without frame offset and optionally deletes the selection to give a cut to clipboard effect. This operator overrides the default Blender copy method which includes cursor offset when pasting, which is atypical of copy/paste methods.',
            'shortcuts': ['Ctrl C; Copy selected strips', 'Ctrl X; Cut selected strips'],
            'demo': 'https://i.imgur.com/w6z1Jb1.gif',
        },
        'power_sequencer.cycle_scenes': {
            'name': 'Cycle Scenes',
            'description': 'Cycle through scenes.',
            'shortcuts': ['Shift TAB; Cycle scenes'],
            'demo': 'https://i.imgur.com/7zhq8Tg.gif',
        },
        'power_sequencer.decrease_playback_speed': {
            'name': 'Decrease Playback Speed',
            'description': 'Playback speed may be set to any of the following speeds:\n\n* Normal (1x)\n* Fast (1.33x)\n* Faster (1.66x)\n* Double (2x)\n* Triple (3x)\n\nActivating this operator will decrease playback speed through each of these steps until minimum speed is reached.',
            'shortcuts': ['LEFT_BRACKET; Decrease Playback Speed'],
            'demo': '',
        },
        'power_sequencer.delete_direct': {
            'name': 'Delete Direct',
            'description': 'Delete without confirmation. Replaces default Blender setting',
            'shortcuts': ['X; Delete direct', 'DEL; Delete direct'],
            'demo': '',
        },
        'power_sequencer.edit_crossfade': {
            'name': 'Edit Crossfade',
            'description': "Selects the handles of both inputs of a crossfade strip's input and calls the grab operator. Allows you to quickly change the location of a fade transition between two strips.",
            'shortcuts': ['Alt C; Edit Crossfade'],
            'demo': '',
        },
        'power_sequencer.fade_strips': {
            'name': 'Fade Strips',
            'description': 'Animate a strips opacity to zero. By default, the duration of the fade is 0.5 seconds.',
            'shortcuts': ['Alt F; Fade Right', 'Ctrl F; Fade Left', 'F; Fade Both'],
            'demo': 'https://i.imgur.com/XoUM2vw.gif',
        },
        'power_sequencer.grab_closest_handle_or_cut': {
            'name': 'Grab Closest Handle or Cut',
            'description': 'Selects and grabs the strip handle or cut closest to the mouse cursor. Hover near a cut and fire this tool to slide it.',
            'shortcuts': ['Shift Alt G;Grab closest handle or cut'],
            'demo': '',
        },
        'power_sequencer.grab_sequence_handle': {
            'name': 'Grab Sequence Handle',
            'description': "Extends the sequence based on the mouse position. If the cursor is to the right of the sequence's middle, it moves the right handle. If it's on the left side, it moves the left handle.",
            'shortcuts': ['Shift G; Grab sequence handles'],
            'demo': '',
        },
        'power_sequencer.import_local_footage': {
            'name': 'Import Local Footage',
            'description': 'Finds the first empty channel above all others in the VSE and returns it',
            'shortcuts': ['Ctrl Shift I; Import Local Footage'],
            'demo': '',
        },
        'power_sequencer.increase_playback_speed': {
            'name': 'Increase Playback Speed',
            'description': 'Playback speed may be set to any of the following speeds:\n\n* Normal (1x)\n* Fast (1.33x)\n* Faster (1.66x)\n* Double (2x)\n* Triple (3x)\n\nActivating this operator will increase playback speed through each of these steps until maximum speed is reached.',
            'shortcuts': ['RIGHT_BRACKET; Increase playback speed'],
            'demo': '',
        },
        'power_sequencer.mouse_cut': {
            'name': 'Mouse Cut',
            'description': 'Quickly cut and remove a section of strips while keeping or collapsing the remaining gap.',
            'shortcuts': ['Ctrl LEFTMOUSE; Cut on mousemove, keep gap', 'Ctrl Shift LEFTMOUSE; Cut on mousemove, remove gap'],
            'demo': 'https://i.imgur.com/wVvX4ex.gif',
        },
        'power_sequencer.mouse_toggle_mute': {
            'name': 'Mouse Toggle Mute',
            'description': 'Toggle mute a sequence as you click on it',
            'shortcuts': ['Alt LEFTMOUSE; Mouse toggle mute'],
            'demo': '',
        },
        'power_sequencer.mouse_trim': {
            'name': 'Mouse Trim',
            'description': "Trims a frame range or a selection from a start to an end frame. If there's no precise time range, auto trims based on the closest cut",
            'shortcuts': ['Ctrl RIGHTMOUSE; Trim strip, keep gap', 'Ctrl Shift RIGHTMOUSE; Trim strip, remove gap'],
            'demo': '',
        },
        'power_sequencer.preview_last_cut': {
            'name': 'Preview Last Cut',
            'description': 'Finds the closest cut to the time cursor and sets the preview to a small range around that frame. If the preview matches the range, resets to the full timeline',
            'shortcuts': ['Shift P; Preview last cut'],
            'demo': '',
        },
        'power_sequencer.preview_to_selection': {
            'name': 'Preview to selection',
            'description': 'Sets the scene frame start to the earliest frame start of selected sequences and the scene frame end to the last frame of selected sequences.',
            'shortcuts': ['Ctrl Alt P; Preview to selection'],
            'demo': 'https://i.imgur.com/EV1sUrn.gif',
        },
        'power_sequencer.render_for_web': {
            'name': 'Render for Web',
            'description': 'Render video with good settings for web upload',
            'shortcuts': ['Alt F12; Render for web'],
            'demo': '',
        },
        'power_sequencer.ripple_delete': {
            'name': 'Ripple Delete',
            'description': 'Delete selected strips and collapse remaining gaps.',
            'shortcuts': ['Shift X; Ripple delete'],
            'demo': '',
        },
        'power_sequencer.save_direct': {
            'name': 'Save Direct',
            'description': 'Save without confirmation, overrides Blender default',
            'shortcuts': ['Ctrl S; Save direct'],
            'demo': '',
        },
        'power_sequencer.smart_snap': {
            'name': 'Smart Snap',
            'description': 'Trims, extends and snaps selected strips to cursor',
            'shortcuts': ['Ctrl K; Smart snap'],
            'demo': '',
        },
        'power_sequencer.snap_selection_to_cursor': {
            'name': 'Snap Selection to Cursor',
            'description': 'Snap selected strips to cursor',
            'shortcuts': ['Alt S; Snap selection to cursor'],
            'demo': '',
        },
        'power_sequencer.toggle_selected_mute': {
            'name': 'Toggle Selected Mute',
            'description': 'Mute or unmute selected strip',
            'shortcuts': ['H;Mute or unmute selected strip'],
            'demo': '',
        },
        'power_sequencer.toggle_waveforms': {
            'name': 'Toggle Waveforms',
            'description': 'Toggle auio waveforms for selected audio strips',
            'shortcuts': ['Alt W; Toggle waveforms'],
            'demo': 'https://i.imgur.com/HJ5ryhv.gif',
        },
        'power_sequencer.trim_to_surrounding_cuts': {
            'name': 'Trim to Surrounding Cuts',
            'description': '',
            'shortcuts': ['Shift Alt LEFTMOUSE; Trim to surrounding cuts'],
            'demo': '',
        },
        'sequencer.refresh_all': {
            'name': 'Refresh All',
            'description': '',
            'shortcuts': ['Shift R; Refresh All'],
            'demo': '',
        },
    }

    toc_title = "<h2>Operators</h2>"

    table_of_contents = make_toc(operator_info)

    operator_segments = make_operator_segments(operator_info)

    html = '\n'.join([title, intro, toc_title, table_of_contents, operator_segments])

    lines = html.split('\n')
    for i in range(len(lines)):
        lines[i] = '    ' + lines[i]

    readme = '.. raw:: html\n\n' + '\n'.join(lines)

    with open(readme_path, 'w') as f:
        f.write(readme)

if __name__ == "__main__":
    make_readme()
