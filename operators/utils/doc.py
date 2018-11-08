import re


def doc_idname(s, prefix='power_sequencer'):
    return prefix + '.' + s.lower().replace(' ', '_')


def doc_name(s):
    return ' '.join(re.findall('[A-Z][^A-Z]*', s))


def doc_brief(s):
    return ' '.join(s.split('\n\n')[0].split()[1:]) if s.startswith('*brief*') else s


def doc_description(s):
    return '\n'.join(map(lambda x: x.strip(), s.split('\n'))).strip()

