import bpy
import operator as op
from .. import operators as ops
from itertools import groupby


keymaps_meta = {
    'Frames': 'EMPTY',
    'Sequencer': 'SEQUENCE_EDITOR'
}


def set_keymap_property(properties, property_name, value):
    try:
        setattr(properties, property_name, value)
    except AttributeError:
        print("Warning: property '%s' not found in keymap item '%s'" %
              (property_name, properties.__class__.__name__))
    except Exception as e:
        print("Warning: %r" % e)


def register_shortcuts():
    def keymapgetter(o):
        return o[1]['keymap']

    os = dir(ops)
    os = filter(lambda o: o[0].isupper(), os)
    os = map(lambda o: op.attrgetter(o), os)
    os = map(lambda o: o(ops), os)
    os = map(lambda o: op.attrgetter('bl_idname', 'doc')(o), os)
    os = {k: v for k, v in os if v != {}}
    os.update(ops.doc)
    os = sorted(os.items(), key=keymapgetter)
    os = groupby(os, key=keymapgetter)

    kms = []
    wm = bpy.context.window_manager
    for name, group in os:
        km = wm.keyconfigs.addon.keymaps.new(name=name, space_type=keymaps_meta[name])
        for bl_idname, d in group:
            for s in d['shortcuts']:
                kmi = km.keymap_items.new(bl_idname, **s[0])
                for pn, pv in s[1].items():
                    set_keymap_property(kmi.properties, pn, pv)
                kms.append((km, kmi))
    return kms

