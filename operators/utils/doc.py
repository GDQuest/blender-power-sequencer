import re


upper_match = lambda m: m.string


def doc_idname(s):
    out = '.'.join(map(str.lower, s.split('_OT_')))
    return out


def doc_name(s):
    out = s.split('_OT')[-1]
    out = re.sub('_[a-z]', lambda m: m[0][1:].upper(), s)
    return out


def doc_brief(s):
    return ' '.join(s.split('\n\n')[0].split()[1:]) if s.startswith('*brief*') else s


def doc_description(s):
    return '\n'.join(map(lambda x: x.strip(), s.split('\n'))).strip()

