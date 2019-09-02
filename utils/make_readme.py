#
# Copyright (C) 2016-2019 by Nathan Lovato, Daniel Oakey, Razvan Radulescu, and contributors
#
# This file is part of Power Sequencer.
#
# Power Sequencer is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Power Sequencer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Power Sequencer. If
# not, see <https://www.gnu.org/licenses/>.
#
import math
import os
import json
from markdown2 import markdown

SHORTCUTS_JSON_FILE = "../scripts/ShortcutsDocs/shortcuts_docs.json"


def make_toc_label(label, description):
    """
    Make a table-of-contents item with a link to the operator and
    description for it's tooltip.
    """
    description = reflow_paragraph(description, 31)

    hla = label.replace(" ", "_")
    html_link = "".join(
        ['<a name="top_', hla, '" href="#', hla, '" title="' + description + '">', label, "</a>"]
    )
    return html_link


def reflow_paragraph(text, space, leading_space=""):
    """
    Reflow a flattened paragraph so it fits inside horizontal
    space
    """
    words = text.split(" ")
    growing_string = leading_space
    output_list = []

    while len(words) > 0:
        if growing_string == leading_space:
            growing_string += words[0]
            words.pop(0)
        elif len(growing_string + " " + words[0]) <= space:
            growing_string += " " + words[0]
            words.pop(0)
        else:
            output_list.append(growing_string + "\n")
            growing_string = leading_space
    output_list.append(growing_string)
    return "".join(output_list)


def make_toc(info):
    """
    Generate a table of contents from the operator info
    """
    toc = ["<table>"]

    labels = []

    for key in sorted(info.keys()):
        label = info[key]["name"]
        description = info[key]["description"]
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
    column_width = str(int((1 / len(columns)) * 888)) + "px"
    for row in range(row_count):
        toc.append("    <tr>")

        for col in range(len(columns)):
            try:
                toc.append("        <td width=" + column_width + ">" + columns[col][row] + "</td>")
            except IndexError:
                if dead_column is False:
                    remaining_rows = row_count - row
                    toc.append(
                        "        <td width="
                        + column_width
                        + ' rowspan="'
                        + str(remaining_rows)
                        + '"></td>'
                    )
                    dead_column = True
        toc.append("    </tr>")
    toc.append("</table>")

    return "\n".join(toc)


def make_seg_label(label):
    """
    Make the title label for an operator segment with a link back to the
    matching table of contents label
    """
    hla = label.replace(" ", "_")
    seg_label = "".join(
        ["    ", "<h3>", '<a name="', hla, '" href="#top_', hla, '">', label, "</a>", "</h3>"]
    )
    return seg_label


def make_shortcuts_table(op_dict):
    """
    Make a table showing all the keyboard shortcuts, their functions,
    and a demo for a given operator
    """
    shortcuts = op_dict["shortcuts"]
    functions = []
    demo = op_dict["demo"]

    for i in range(len(shortcuts)):
        hotkeys = shortcuts[i].split(" ")
        for x in range(len(hotkeys)):
            hotkeys[x] = (
                '<img src="https://cdn.rawgit.com/doakey3/Keyboard-SVGs/master/images/'
                + hotkeys[x].strip().upper()
                + '.png" alt="'
                + hotkeys[x].strip().upper()
                + '">'
            )
        shortcuts[i] = "".join(hotkeys)

    hotkeys_width = str(int((888 - 256) * 0.33)) + "px"
    function_width = str(int((888 - 256) * 0.66)) + "px"
    table = ["<table>"]
    table.append("    <tr>")
    table.append("        <th width=" + hotkeys_width + ">Shortcut</th>")

    if len(functions) > 0:
        table.append("        <th width=" + function_width + ">Function</th>")
    if demo != "":
        table.append("        <th width=256px>Demo</th>")

    for i in range(len(shortcuts)):
        table.append("    <tr>")

        table.append('        <td align="center">' + "".join(shortcuts[i]) + "</td>")
        table.append("        <td>" + markdown(functions[i]) + "</td>")

        if i == 0 and demo != "":
            table.append(
                '        <td align="center" rowspan="'
                + str(len(shortcuts))
                + '">'
                + '<img src="'
                + demo
                + '"></td>'
            )

        table.append("    </tr>")
    table.append("</table>")
    return "\n".join(table)


def make_operator_segments(info):
    """
    Using the operator info, make segments that put all that info together.
    """
    segments = []

    for key in sorted(info.keys()):
        label = make_seg_label(info[key]["name"])
        description = markdown(info[key]["description"])
        shortcut_table = make_shortcuts_table(info[key])

        segments.append("\n".join([label, description, shortcut_table]))
    return "\n".join(segments)


def make_readme():
    """
    Generate a nice-looking readme.
    """
    readme_path = "README.rst"
    title = """
<h1 align="center">
  Blender Power Sequencer</br>
  <small>The Free add-on for content creators</small>
</h1>

<p align='center'>
  <img src="https://i.imgur.com/LbxKduw.png" alt="Power Sequencer logo, with the add-on's name and strips cut in two" />
</p>
"""

    intro = markdown(
        """
    Power Sequencer brings smart new editing features to edit faster with Blender's Video Sequence Editor. It is completely Free and Open Source.

## Contributing ##

All contributors are welcome! We need people to:

- Code new features
- Improve existing features
- Help solidify the code
- Write mini-tutorials

You can come and chat with us on [GDquest's Discord server](https://discordapp.com/invite/87NNb3Z)!

See our [Contributor's Guidelines](http://gdquest.com/open-source/contributing-guidelines/) to get started contributing. We also have a [Code of Conduct](http://gdquest.com/open-source/code-of-conduct/) based on the GNU Kind Communication Guidelines.

Join the discussion in the [issues tab](https://github.com/GDquest/Blender-power-sequencer/issues)

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

## Learn Power Sequencer ##

Watch our growing list of [Free video
tutorials](https://www.youtube.com/playlist?list=PLhqJJNjsQ7KFjp88Cu57Zb9_wFt7nlkEI)
on Youtube!

You can also find all the features and shortcuts on the [Power Sequencer Docs](http://gdquest.com/blender/power-sequencer/docs/)

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
""".strip(),
        extras=["cuddled_lists"],
    )

    operator_info = {}
    this_folder = os.path.split(__file__)[0]
    json_path = os.path.abspath(os.path.join(this_folder, SHORTCUTS_JSON_FILE))
    assert os.path.exists(json_path)
    with open(json_path, "r") as json_file:
        operator_info = json.load(json_file)
    if operator_info == {}:
        return

    # TODO: add support for the new shortcuts json format
    # TODO: try to use markdown directly instead of html
    # toc_title = "<h2>Operators</h2>"
    # table_of_contents = make_toc(operator_info)
    # operator_segments = make_operator_segments(operator_info)
    # html = '\n'.join([title, intro, toc_title, table_of_contents, operator_segments])

    html = "\n".join([title, intro])
    lines = html.split("\n")
    for i in range(len(lines)):
        lines[i] = "    " + lines[i]
    readme = ".. raw:: html\n\n" + "\n".join(lines)

    with open(readme_path, "w") as f:
        f.write(readme)


if __name__ == "__main__":
    make_readme()
