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
import json
import operator as op
import os.path
import sys

import power_sequencer.operators as operators

sys.path.append(os.path.abspath(os.path.join("..", "..", "..")))



if __name__ == "__main__":
    os = dir(operators)
    os = filter(lambda o: o[0].isupper(), os)
    os = map(lambda o: op.attrgetter(o), os)
    os = map(lambda o: o(operators), os)
    os = map(lambda o: op.attrgetter("bl_idname", "doc")(o), os)
    os = {k: v for k, v in os if v != {}}
    os.update(operators.doc)

    json.dump(os, open("power_sequencer_docs.json", "w"), indent=4, sort_keys=True)
