#
# Copyright (C) 2016-2020 by Nathan Lovato, Daniel Oakey, Razvan Radulescu, and contributors
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
from os.path import abspath, join
import sys

import power_sequencer.operators as operators

sys.path.append(abspath(join("..", "..", "..")))


if __name__ == "__main__":
    data = {}
    for operator in operators.get_operator_classes():
        idname = getattr(operator, "bl_idname")
        data[idname] = operator.doc
    json.dump(data, open("power_sequencer_docs.json", "w"), indent=4, sort_keys=True)
