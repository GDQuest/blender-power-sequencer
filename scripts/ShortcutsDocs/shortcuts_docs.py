import json
import operator as op
import os.path
import sys

sys.path.append(os.path.abspath(os.path.join("..", "..")))

import operators as ops


if __name__ == "__main__":
    os = dir(ops)
    os = filter(lambda o: o[0].isupper(), os)
    os = map(lambda o: op.attrgetter(o), os)
    os = map(lambda o: o(ops), os)
    os = map(lambda o: op.attrgetter("bl_idname", "doc")(o), os)
    os = {k: v for k, v in os if v != {}}
    os.update(ops.doc)

    json.dump(os, open("shortcuts_docs.json", "w"), indent=4, sort_keys=True)
