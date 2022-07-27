# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2016-2020 by Nathan Lovato, Daniel Oakey, Razvan Radulescu, and contributors
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
