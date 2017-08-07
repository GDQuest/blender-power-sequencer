import json

operators = {}
py_strings = []

with open('power_sequencer_menu.json', mode='r') as data:
    json_string = data.read()
    parsed_json = json.loads(json_string)
    for level_1 in parsed_json:
        for level_2 in level_1:
            for level_3 in level_2:
                if len(level_3)>1:
                    count = 0
                    function_name, icon, operator = '', '', ''
                    for entry in level_3:
                        if count == 0:
                            function_name = entry
                        elif count == 1:
                            pass
                        elif count == 2:
                            icon = entry
                        elif count == 3:
                            operator = entry.replace('bpy.ops.', '')[:-2]
                        count += 1
                    py_string = "layout.operator('{!s}', icon='{!s}', text='{!s}')".format(operator, icon, function_name)
                    py_strings.append(py_string)
                    print(py_string)
for string in py_strings:
    print(string)
