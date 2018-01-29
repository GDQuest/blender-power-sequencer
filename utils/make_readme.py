import os
from markdown2 import markdown

from readutils.make_op_segments import make_op_segments
from readutils.make_op_toc import make_op_toc
from docjson import make_json

def make_toc_labels(labels):
    for i in range(len(labels)):
        hla = labels[i].replace(' ', '_')
        labels[i] = '<a name="top_' + hla + '" href="#' + hla + '">' + labels[i] + '</a>'
    return labels

output_path = os.path.join(os.getcwd(), '../', 'README.rst')
ops_path = os.path.join(os.getcwd(), '../', 'operators')
info = make_json(ops_path)

op_toc = make_op_toc(info)
op_segments = make_op_segments(info)

title = """
<h1 align="center">
  Blender Power Sequencer</br>
  <small>The Free add-on for content creators</small>
</h1>

<p align='center'>
  <img src="https://i.imgur.com/6tVdzBQ.jpg" alt="Power Sequencer logo, with the add-on's name and strips cut in two" />
</p>
"""

installation = markdown("""
I've made [hundreds of tutorials](http://youtube.com/c/gdquest) over the
years. After working with popular professional programs like Vegas and
Resolve, I now **work exclusively with Blender**. It does have some
limitations, but it's the most stable and versatile tool you'll find out
there.

I built Power Sequencer to help us edit videos as fast as possible. The
add-on is getting better month after month, and it's yours for Free.

I've made hundreds of tutorials over the years. 

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
""".strip())

readme = '\n'.join([title, installation, "<h2>Operators</h2>", op_toc, op_segments])
lines = readme.split('\n')

for i in range(len(lines)):
    lines[i] = '    ' + lines[i]

readme = '.. raw:: html\n\n' + '\n'.join(lines)

with open(output_path, 'w') as f:
    f.write(readme)


