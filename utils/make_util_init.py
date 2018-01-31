"""
A rough script for making a __init__.py for a folder containing
utils. (Goes through each file and imports the function from that
file that equals the name of the file.

To use it, place this script into the folder containing the operators
and run it.
"""

import os

files = []
for file in os.listdir(os.getcwd()):
    if file.endswith('.py') and not file in ['_make_util_init.py', '__init__.py']:
        
        fname = os.path.splitext(file)[0]
        
        files.append('from .' + fname + ' import ' + fname)

f = open('__init__.py', 'w')
f.write('\n'.join(sorted(files)))
f.close()
        
