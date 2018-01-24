import os

def capitalize(word):
    if len(word) > 1:
        word = word[0].upper() + word[1::]
        return word
    else:
        return word.upper()


for file in os.listdir(os.getcwd()):
    if file.endswith('.py') and not file == 'consistency_checker.py':
        fname = os.path.splitext(file)[0]
        expected_classname_split = fname.split('_')
        for i in range(len(expected_classname_split)):
            expected_classname_split[i] = capitalize(expected_classname_split[i])
        
        expected_classname = ''.join(expected_classname_split)
        
        expected_idname = 'power_sequencer.' + fname
        
        label_split = fname.split('_')
        label_split[0] = capitalize(label_split[0])
        expected_label = 'PS.' + ' '.join(label_split)
        
        #print(expected_classname, expected_idname, expected_label)
        
        
        with open(file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.lstrip().startswith('bl_label'):
                if not expected_label in line:
                    print(file)
