def indent_json(dictionary, indent=0):
    """
    Makes an indented json string out of a dictionary,
    but non dictionary elements are not indented.
    """
    lines = []

    keys = sorted(list(dictionary.keys()))
    for i in range(len(keys)):
        key = keys[i]
        if type(dictionary[key]) is dict:
            lines.append(' ' * indent + '"' + key + '" : {')
            lines.extend(indent_json(dictionary[key], indent + 4))
            lines.append(' ' * indent + '}')
        else:
            list_string = '['
            for x in range(len(dictionary[key])):
                item = dictionary[key][x]
                if x < len(dictionary[key]) - 1:
                    list_string += '"' + item + '", '
                else:
                    list_string += '"' + item + '"'
            list_string += ']'
            lines.append(' ' * indent + '"' + key + '" : ' + list_string)

        if not i == len(keys) - 1:
                lines[-1] += ','

    return lines

def pretty_json(dictionary):
    """
    Make a json file that is reader-friendly
    """
    output = ['{', '\n'.join(indent_json(dictionary, indent=4)), '}']
    return '\n'.join(output)
