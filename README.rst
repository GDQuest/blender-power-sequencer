.. raw:: html

    <h1 align="center">
      Blender Power Sequencer</br>
      <small>The Free add-on for content creators</small>
    </h1>

    <p align='center'>
      <img src="https://i.imgur.com/LbxKduw.png" alt="Power Sequencer logo, with the add-on's name and strips cut in two" />
    </p>

    <p>Power Sequencer brings smart new editing features to edit faster with Blender's Video Sequence Editor. It is completely Free and Open Source.</p>

    <h2>Contributing</h2>

    <p>All contributors are welcome! We need people to:</p>

    <ul>
    <li>Code new features</li>
    <li>Improve existing features</li>
    <li>Help solidify the code</li>
    <li>Write mini-tutorials</li>
    </ul>

    <p>You can come and chat with us on <a href="https://discordapp.com/invite/87NNb3Z">GDquest's Discord server</a>!</p>

    <p>See our <a href="http://gdquest.com/open-source/contributing-guidelines/">Contributor's Guidelines</a> to get started contributing. We also have a <a href="http://gdquest.com/open-source/code-of-conduct/">Code of Conduct</a> based on the GNU Kind Communication Guidelines.</p>

    <p>Join the discussion in the <a href="https://github.com/GDquest/Blender-power-sequencer/issues">issues tab</a></p>

    <h2>Installation</h2>

    <ol>
    <li>Download the repository. Go to
    <a href="https://github.com/GDquest/Blender-power-sequencer/releases">Releases</a>
    for a stable version, or click the green button above to get the most
    recent (and potentially unstable) version.</li>
    <li>Open Blender</li>
    <li>Go to File &gt; User Preferences &gt; Addons</li>
    <li>Click "Install From File" and navigate to the downloaded .zip file
    and install</li>
    <li>Check the box next to "VSE: Power Sequencer"</li>
    <li>Save User Settings so the addon remains active every time you open
    Blender</li>
    </ol>

    <h2>Learn Power Sequencer</h2>

    <p>Watch our growing list of <a href="https://www.youtube.com/playlist?list=PLhqJJNjsQ7KFjp88Cu57Zb9_wFt7nlkEI">Free video
    tutorials</a>
    on Youtube!</p>

    <p>You can also find all the features and shortcuts on the <a href="http://gdquest.com/blender/power-sequencer/docs/">Power Sequencer Docs</a></p>

    <h2>Other add-ons</h2>

    <p>Here are other recommended add-ons for a better editing workflow:</p>

    <p>Daniel Oakey's <a href="https://github.com/doakey3/VSE_Transform_Tools">rewrite of VSE Transform Tools</a>.
    This tool lets you animate and move strips from the video preview. The
    original add-on was abandoned a few years ago. Daniel fixed and rewrote
    it so now it's super slick!</p>

    <h2>Credits</h2>

    <ul>
    <li><a href="https://github.com/davcri">davcri</a></li>
    <li><a href="https://github.com/doakey3">Daniel Oakey</a></li>
    <li><a href="https://twitter.com/NathanGDquest"> Nathan Lovato </a></li>
    </ul>


    <h2>Operators</h2>
    <table>
        <tr>
            <td width=222px><a name="top_Add_Crossfade" href="#Add_Crossfade" title="Based on the active strip,
    finds the closest next sequence
    of a similar type, moves it so
    it overlaps the active strip,
    and adds a gamma cross effect
    between them. Works with MOVIE,
    IMAGE and META strips">Add Crossfade</a></td>
            <td width=222px><a name="top_Copy_Selected_Sequences" href="#Copy_Selected_Sequences" title="Copies the selected sequences
    without frame offset and
    optionally deletes the
    selection to give a cut to
    clipboard effect. This operator
    overrides the default Blender
    copy method which includes
    cursor offset when pasting,
    which is atypical of copy/paste
    methods.">Copy Selected Sequences</a></td>
            <td width=222px><a name="top_Import_Local_Footage" href="#Import_Local_Footage" title="Finds the first empty channel
    above all others in the VSE and
    returns it">Import Local Footage</a></td>
            <td width=222px><a name="top_Ripple_Delete" href="#Ripple_Delete" title="Delete selected strips and
    collapse remaining gaps.">Ripple Delete</a></td>
        </tr>
        <tr>
            <td width=222px><a name="top_Add_Speed" href="#Add_Speed" title="Add 2x speed to strip and set
    it's frame end accordingly.
    Wraps both the strip and the
    speed modifier into a META
    strip.">Add Speed</a></td>
            <td width=222px><a name="top_Cycle_Scenes" href="#Cycle_Scenes" title="Cycle through scenes.">Cycle Scenes</a></td>
            <td width=222px><a name="top_Increase_Playback_Speed" href="#Increase_Playback_Speed" title="Playback speed may be set to
    any of the following speeds:

    *
    Normal (1x)
    * Fast (1.33x)
    *
    Faster (1.66x)
    * Double (2x)
    *
    Triple (3x)

    Activating this
    operator will increase playback
    speed through each of these
    steps until maximum speed is
    reached.">Increase Playback Speed</a></td>
            <td width=222px><a name="top_Save_Direct" href="#Save_Direct" title="Save without confirmation,
    overrides Blender default">Save Direct</a></td>
        </tr>
        <tr>
            <td width=222px><a name="top_Add_Transform" href="#Add_Transform" title="For each strip in the
    selection:

    * Filters the
    selection down to image and
    movie strips
    * Centers the
    pivot point of image strips
    *
    Adds a transform effect and
    sets it to ALPHA_OVER">Add Transform</a></td>
            <td width=222px><a name="top_Decrease_Playback_Speed" href="#Decrease_Playback_Speed" title="Playback speed may be set to
    any of the following speeds:

    *
    Normal (1x)
    * Fast (1.33x)
    *
    Faster (1.66x)
    * Double (2x)
    *
    Triple (3x)

    Activating this
    operator will decrease playback
    speed through each of these
    steps until minimum speed is
    reached.">Decrease Playback Speed</a></td>
            <td width=222px><a name="top_Mouse_Cut" href="#Mouse_Cut" title="Quickly cut and remove a
    section of strips while keeping
    or collapsing the remaining
    gap.">Mouse Cut</a></td>
            <td width=222px><a name="top_Smart_Snap" href="#Smart_Snap" title="Trims, extends and snaps
    selected strips to cursor">Smart Snap</a></td>
        </tr>
        <tr>
            <td width=222px><a name="top_Border_Select" href="#Border_Select" title="Deselects the strips' handles
    before applying border select,
    so you don't have to deselect
    manually first">Border Select</a></td>
            <td width=222px><a name="top_Delete_Direct" href="#Delete_Direct" title="Delete without confirmation.
    Replaces default Blender
    setting">Delete Direct</a></td>
            <td width=222px><a name="top_Mouse_Toggle_Mute" href="#Mouse_Toggle_Mute" title="Toggle mute a sequence as you
    click on it">Mouse Toggle Mute</a></td>
            <td width=222px><a name="top_Snap_Selection_to_Cursor" href="#Snap_Selection_to_Cursor" title="Snap selected strips to cursor">Snap Selection to Cursor</a></td>
        </tr>
        <tr>
            <td width=222px><a name="top_Change_Playback_Speed" href="#Change_Playback_Speed" title="Change the playback_speed
    property using an operator
    property. Used with keymaps">Change Playback Speed</a></td>
            <td width=222px><a name="top_Edit_Crossfade" href="#Edit_Crossfade" title="Selects the handles of both
    inputs of a crossfade strip's
    input and calls the grab
    operator. Allows you to quickly
    change the location of a fade
    transition between two strips.">Edit Crossfade</a></td>
            <td width=222px><a name="top_Mouse_Trim" href="#Mouse_Trim" title="Trims a frame range or a
    selection from a start to an
    end frame. If there's no
    precise time range, auto trims
    based on the closest cut">Mouse Trim</a></td>
            <td width=222px><a name="top_Toggle_Selected_Mute" href="#Toggle_Selected_Mute" title="Mute or unmute selected strip">Toggle Selected Mute</a></td>
        </tr>
        <tr>
            <td width=222px><a name="top_Channel_Offset" href="#Channel_Offset" title="Move selected strip to the
    nearest open channel above/down">Channel Offset</a></td>
            <td width=222px><a name="top_Fade_Strips" href="#Fade_Strips" title="Animate a strips opacity to
    zero. By default, the duration
    of the fade is 0.5 seconds.">Fade Strips</a></td>
            <td width=222px><a name="top_Preview_Last_Cut" href="#Preview_Last_Cut" title="Finds the closest cut to the
    time cursor and sets the
    preview to a small range around
    that frame. If the preview
    matches the range, resets to
    the full timeline">Preview Last Cut</a></td>
            <td width=222px><a name="top_Toggle_Waveforms" href="#Toggle_Waveforms" title="Toggle auio waveforms for
    selected audio strips">Toggle Waveforms</a></td>
        </tr>
        <tr>
            <td width=222px><a name="top_Clear_Fades" href="#Clear_Fades" title="Set strip opacity to 1.0 and
    remove all opacity-keyframes">Clear Fades</a></td>
            <td width=222px><a name="top_Grab_Closest_Handle_or_Cut" href="#Grab_Closest_Handle_or_Cut" title="Selects and grabs the strip
    handle or cut closest to the
    mouse cursor. Hover near a cut
    and fire this tool to slide it.">Grab Closest Handle or Cut</a></td>
            <td width=222px><a name="top_Preview_to_selection" href="#Preview_to_selection" title="Sets the scene frame start to
    the earliest frame start of
    selected sequences and the
    scene frame end to the last
    frame of selected sequences.">Preview to selection</a></td>
            <td width=222px><a name="top_Trim_to_Surrounding_Cuts" href="#Trim_to_Surrounding_Cuts" title="">Trim to Surrounding Cuts</a></td>
        </tr>
        <tr>
            <td width=222px><a name="top_Concatenate_Strips" href="#Concatenate_Strips" title="Concatenates selected strips in
    a channel (removes the gap
    between them) If a single strip
    is selected, either the next
    strip in the channel will be
    concatenated, or all strips in
    the channel will be
    concatenated depending on which
    shortcut is used.">Concatenate Strips</a></td>
            <td width=222px><a name="top_Grab_Sequence_Handles" href="#Grab_Sequence_Handles" title="Extends the sequence based on
    the mouse position. If the
    cursor is to the right of the
    sequence's middle, it moves the
    right handle. If it's on the
    left side, it moves the left
    handle.">Grab Sequence Handle</a></td>
            <td width=222px><a name="top_Render_for_Web" href="#Render_for_Web" title="Render video with good settings
    for web upload">Render for Web</a></td>
            <td width=222px><a name="top_Refresh_All" href="#Refresh_All" title="">Refresh All</a></td>
        </tr>
    </table>
        <h3><a name="Add_Crossfade" href="#top_Add_Crossfade">Add Crossfade</a></h3>
    <p>Based on the active strip, finds the closest next sequence of a similar type, moves it so it overlaps the active strip, and adds a gamma cross effect between them. Works with MOVIE, IMAGE and META strips</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
            <th width=256px>Demo</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/CTRL.png" alt="CTRL"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/C.png" alt="C"></td>
            <td><p>Add Crossfade</p>
    </td>
            <td align="center" rowspan="1"><img src="https://i.imgur.com/ZyEd0jD.gif"></td>
        </tr>
    </table>
        <h3><a name="Add_Speed" href="#top_Add_Speed">Add Speed</a></h3>
    <p>Add 2x speed to strip and set its frame end accordingly. Wraps both the strip and the speed modifier into a META strip.</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
            <th width=256px>Demo</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/SHIFT.png" alt="SHIFT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/PLUS.png" alt="PLUS"></td>
            <td><p>Add Speed</p>
    </td>
            <td align="center" rowspan="1"><img src="https://i.imgur.com/lheIZzA.gif"></td>
        </tr>
    </table>
        <h3><a name="Add_Transform" href="#top_Add_Transform">Add Transform</a></h3>
    <p>For each strip in the selection:</p>

    <ul>
    <li>Filters the selection down to image and movie strips</li>
    <li>Centers the pivot point of image strips</li>
    <li>Adds a transform effect and sets it to ALPHA_OVER</li>
    </ul>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/T.png" alt="T"></td>
            <td><p>Add Transform</p>
    </td>
        </tr>
    </table>
        <h3><a name="Border_Select" href="#top_Border_Select">Border Select</a></h3>
    <p>Deselects the strips' handles before applying border select, so you don't have to deselect manually first</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/SHIFT.png" alt="SHIFT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/B.png" alt="B"></td>
            <td><p>Border Select</p>
    </td>
        </tr>
    </table>
        <h3><a name="Change_Playback_Speed" href="#top_Change_Playback_Speed">Change Playback Speed</a></h3>
    <p>Change the playback_speed property using an operator property. Used with keymaps</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ONE.png" alt="ONE"></td>
            <td><p>Speed to 1x</p>
    </td>
        </tr>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/TWO.png" alt="TWO"></td>
            <td><p>Speed to 1.33x</p>
    </td>
        </tr>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/THREE.png" alt="THREE"></td>
            <td><p>Speed to 1.66x</p>
    </td>
        </tr>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/FOUR.png" alt="FOUR"></td>
            <td><p>Speed to 2x</p>
    </td>
        </tr>
    </table>
        <h3><a name="Channel_Offset" href="#top_Channel_Offset">Channel Offset</a></h3>
    <p>Move selected strip to the nearest open channel above/down</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/UP_ARROW.png" alt="UP_ARROW"></td>
            <td><p>Move to open channel above</p>
    </td>
        </tr>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/DOWN_ARROW.png" alt="DOWN_ARROW"></td>
            <td><p>Move to open channel above</p>
    </td>
        </tr>
    </table>
        <h3><a name="Clear_Fades" href="#top_Clear_Fades">Clear Fades</a></h3>
    <p>Set strip opacity to 1.0 and remove all opacity-keyframes</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/CTRL.png" alt="CTRL"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/F.png" alt="F"></td>
            <td><p>Clear fades</p>
    </td>
        </tr>
    </table>
        <h3><a name="Concatenate_Strips" href="#top_Concatenate_Strips">Concatenate Strips</a></h3>
    <p>Concatenates selected strips in a channel (removes the gap between them) If a single strip is selected, either the next strip in the channel will be concatenated, or all strips in the channel will be concatenated depending on which shortcut is used.</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
            <th width=256px>Demo</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/C.png" alt="C"></td>
            <td><p>Concatenate selected strips in channel, or concatenate &amp; select next strip in channel if only 1 strip selected</p>
    </td>
            <td align="center" rowspan="2"><img src="https://i.imgur.com/YyEL8YP.gif"></td>
        </tr>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/SHIFT.png" alt="SHIFT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/C.png" alt="C"></td>
            <td><p>Concatenate selected strips in channel, or concatenate all strips in channel if only 1 strip selected</p>
    </td>
        </tr>
    </table>
        <h3><a name="Copy_Selected_Sequences" href="#top_Copy_Selected_Sequences">Copy Selected Sequences</a></h3>
    <p>Copies the selected sequences without frame offset and optionally deletes the selection to give a cut to clipboard effect. This operator overrides the default Blender copy method which includes cursor offset when pasting, which is atypical of copy/paste methods.</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
            <th width=256px>Demo</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/CTRL.png" alt="CTRL"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/C.png" alt="C"></td>
            <td><p>Copy selected strips</p>
    </td>
            <td align="center" rowspan="2"><img src="https://i.imgur.com/w6z1Jb1.gif"></td>
        </tr>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/CTRL.png" alt="CTRL"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/X.png" alt="X"></td>
            <td><p>Cut selected strips</p>
    </td>
        </tr>
    </table>
        <h3><a name="Cycle_Scenes" href="#top_Cycle_Scenes">Cycle Scenes</a></h3>
    <p>Cycle through scenes.</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
            <th width=256px>Demo</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/SHIFT.png" alt="SHIFT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/TAB.png" alt="TAB"></td>
            <td><p>Cycle scenes</p>
    </td>
            <td align="center" rowspan="1"><img src="https://i.imgur.com/7zhq8Tg.gif"></td>
        </tr>
    </table>
        <h3><a name="Decrease_Playback_Speed" href="#top_Decrease_Playback_Speed">Decrease Playback Speed</a></h3>
    <p>Playback speed may be set to any of the following speeds:</p>

    <ul>
    <li>Normal (1x)</li>
    <li>Fast (1.33x)</li>
    <li>Faster (1.66x)</li>
    <li>Double (2x)</li>
    <li>Triple (3x)</li>
    </ul>

    <p>Activating this operator will decrease playback speed through each of these steps until minimum speed is reached.</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/LEFT_BRACKET.png" alt="LEFT_BRACKET"></td>
            <td><p>Decrease Playback Speed</p>
    </td>
        </tr>
    </table>
        <h3><a name="Delete_Direct" href="#top_Delete_Direct">Delete Direct</a></h3>
    <p>Delete without confirmation. Replaces default Blender setting</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/X.png" alt="X"></td>
            <td><p>Delete direct</p>
    </td>
        </tr>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/DEL.png" alt="DEL"></td>
            <td><p>Delete direct</p>
    </td>
        </tr>
    </table>
        <h3><a name="Edit_Crossfade" href="#top_Edit_Crossfade">Edit Crossfade</a></h3>
    <p>Selects the handles of both inputs of a crossfade strip's input and calls the grab operator. Allows you to quickly change the location of a fade transition between two strips.</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/C.png" alt="C"></td>
            <td><p>Edit Crossfade</p>
    </td>
        </tr>
    </table>
        <h3><a name="Fade_Strips" href="#top_Fade_Strips">Fade Strips</a></h3>
    <p>Animate a strips opacity to zero. By default, the duration of the fade is 0.5 seconds.</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
            <th width=256px>Demo</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/F.png" alt="F"></td>
            <td><p>Fade Right</p>
    </td>
            <td align="center" rowspan="3"><img src="https://i.imgur.com/XoUM2vw.gif"></td>
        </tr>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/CTRL.png" alt="CTRL"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/F.png" alt="F"></td>
            <td><p>Fade Left</p>
    </td>
        </tr>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/F.png" alt="F"></td>
            <td><p>Fade Both</p>
    </td>
        </tr>
    </table>
        <h3><a name="Grab_Closest_Handle_or_Cut" href="#top_Grab_Closest_Handle_or_Cut">Grab Closest Handle or Cut</a></h3>
    <p>Selects and grabs the strip handle or cut closest to the mouse cursor. Hover near a cut and fire this tool to slide it.</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/SHIFT.png" alt="SHIFT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/G.png" alt="G"></td>
            <td><p>Grab closest handle or cut</p>
    </td>
        </tr>
    </table>
        <h3><a name="Grab_Sequence_Handles" href="#top_Grab_Sequence_Handles">Grab Sequence Handle</a></h3>
    <p>Extends the sequence based on the mouse position. If the cursor is to the right of the sequence's middle, it moves the right handle. If it's on the left side, it moves the left handle.</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/SHIFT.png" alt="SHIFT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/G.png" alt="G"></td>
            <td><p>Grab sequence handles</p>
    </td>
        </tr>
    </table>
        <h3><a name="Import_Local_Footage" href="#top_Import_Local_Footage">Import Local Footage</a></h3>
    <p>Finds the first empty channel above all others in the VSE and returns it</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/CTRL.png" alt="CTRL"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/SHIFT.png" alt="SHIFT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/I.png" alt="I"></td>
            <td><p>Import Local Footage</p>
    </td>
        </tr>
    </table>
        <h3><a name="Increase_Playback_Speed" href="#top_Increase_Playback_Speed">Increase Playback Speed</a></h3>
    <p>Playback speed may be set to any of the following speeds:</p>

    <ul>
    <li>Normal (1x)</li>
    <li>Fast (1.33x)</li>
    <li>Faster (1.66x)</li>
    <li>Double (2x)</li>
    <li>Triple (3x)</li>
    </ul>

    <p>Activating this operator will increase playback speed through each of these steps until maximum speed is reached.</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/RIGHT_BRACKET.png" alt="RIGHT_BRACKET"></td>
            <td><p>Increase playback speed</p>
    </td>
        </tr>
    </table>
        <h3><a name="Mouse_Cut" href="#top_Mouse_Cut">Mouse Cut</a></h3>
    <p>Quickly cut and remove a section of strips while keeping or collapsing the remaining gap.</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
            <th width=256px>Demo</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/CTRL.png" alt="CTRL"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/LEFTMOUSE.png" alt="LEFTMOUSE"></td>
            <td><p>Cut on mousemove, keep gap</p>
    </td>
            <td align="center" rowspan="2"><img src="https://i.imgur.com/wVvX4ex.gif"></td>
        </tr>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/CTRL.png" alt="CTRL"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/SHIFT.png" alt="SHIFT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/LEFTMOUSE.png" alt="LEFTMOUSE"></td>
            <td><p>Cut on mousemove, remove gap</p>
    </td>
        </tr>
    </table>
        <h3><a name="Mouse_Toggle_Mute" href="#top_Mouse_Toggle_Mute">Mouse Toggle Mute</a></h3>
    <p>Toggle mute a sequence as you click on it</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/LEFTMOUSE.png" alt="LEFTMOUSE"></td>
            <td><p>Mouse toggle mute</p>
    </td>
        </tr>
    </table>
        <h3><a name="Mouse_Trim" href="#top_Mouse_Trim">Mouse Trim</a></h3>
    <p>Trims a frame range or a selection from a start to an end frame. If there's no precise time range, auto trims based on the closest cut</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/CTRL.png" alt="CTRL"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/RIGHTMOUSE.png" alt="RIGHTMOUSE"></td>
            <td><p>Trim strip, keep gap</p>
    </td>
        </tr>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/CTRL.png" alt="CTRL"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/SHIFT.png" alt="SHIFT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/RIGHTMOUSE.png" alt="RIGHTMOUSE"></td>
            <td><p>Trim strip, remove gap</p>
    </td>
        </tr>
    </table>
        <h3><a name="Preview_Last_Cut" href="#top_Preview_Last_Cut">Preview Last Cut</a></h3>
    <p>Finds the closest cut to the time cursor and sets the preview to a small range around that frame. If the preview matches the range, resets to the full timeline</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/SHIFT.png" alt="SHIFT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/P.png" alt="P"></td>
            <td><p>Preview last cut</p>
    </td>
        </tr>
    </table>
        <h3><a name="Preview_to_selection" href="#top_Preview_to_selection">Preview to selection</a></h3>
    <p>Sets the scene frame start to the earliest frame start of selected sequences and the scene frame end to the last frame of selected sequences.</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
            <th width=256px>Demo</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/CTRL.png" alt="CTRL"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/P.png" alt="P"></td>
            <td><p>Preview to selection</p>
    </td>
            <td align="center" rowspan="1"><img src="https://i.imgur.com/EV1sUrn.gif"></td>
        </tr>
    </table>
        <h3><a name="Render_for_Web" href="#top_Render_for_Web">Render for Web</a></h3>
    <p>Render video with good settings for web upload</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/F12.png" alt="F12"></td>
            <td><p>Render for web</p>
    </td>
        </tr>
    </table>
        <h3><a name="Ripple_Delete" href="#top_Ripple_Delete">Ripple Delete</a></h3>
    <p>Delete selected strips and collapse remaining gaps.</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/SHIFT.png" alt="SHIFT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/X.png" alt="X"></td>
            <td><p>Ripple delete</p>
    </td>
        </tr>
    </table>
        <h3><a name="Save_Direct" href="#top_Save_Direct">Save Direct</a></h3>
    <p>Save without confirmation, overrides Blender default</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/CTRL.png" alt="CTRL"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/S.png" alt="S"></td>
            <td><p>Save direct</p>
    </td>
        </tr>
    </table>
        <h3><a name="Smart_Snap" href="#top_Smart_Snap">Smart Snap</a></h3>
    <p>Trims, extends and snaps selected strips to cursor</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/CTRL.png" alt="CTRL"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/K.png" alt="K"></td>
            <td><p>Smart snap</p>
    </td>
        </tr>
    </table>
        <h3><a name="Snap_Selection_to_Cursor" href="#top_Snap_Selection_to_Cursor">Snap Selection to Cursor</a></h3>
    <p>Snap selected strips to cursor</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/S.png" alt="S"></td>
            <td><p>Snap selection to cursor</p>
    </td>
        </tr>
    </table>
        <h3><a name="Toggle_Selected_Mute" href="#top_Toggle_Selected_Mute">Toggle Selected Mute</a></h3>
    <p>Mute or unmute selected strip</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/H.png" alt="H"></td>
            <td><p>Mute or unmute selected strip</p>
    </td>
        </tr>
    </table>
        <h3><a name="Toggle_Waveforms" href="#top_Toggle_Waveforms">Toggle Waveforms</a></h3>
    <p>Toggle auio waveforms for selected audio strips</p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
            <th width=256px>Demo</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/W.png" alt="W"></td>
            <td><p>Toggle waveforms</p>
    </td>
            <td align="center" rowspan="1"><img src="https://i.imgur.com/HJ5ryhv.gif"></td>
        </tr>
    </table>
        <h3><a name="Trim_to_Surrounding_Cuts" href="#top_Trim_to_Surrounding_Cuts">Trim to Surrounding Cuts</a></h3>
    <p></p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/SHIFT.png" alt="SHIFT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/ALT.png" alt="ALT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/LEFTMOUSE.png" alt="LEFTMOUSE"></td>
            <td><p>Trim to surrounding cuts</p>
    </td>
        </tr>
    </table>
        <h3><a name="Refresh_All" href="#top_Refresh_All">Refresh All</a></h3>
    <p></p>

    <table>
        <tr>
            <th width=208px>Shortcut</th>
            <th width=417px>Function</th>
        <tr>
            <td align="center"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/SHIFT.png" alt="SHIFT"><img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/R.png" alt="R"></td>
            <td><p>Refresh All</p>
    </td>
        </tr>
    </table>
