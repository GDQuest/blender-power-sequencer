import subprocess
import os
import shutil
# import ntpath


def sorter(files_list):
    files_list = sorted(files_list, key=str.lower)
    files = []
    folders = []
    for file in files_list:
        if '.' in file:
            files.append(file)
        else:
            folders.append(file)

    files.extend(folders)
    return files


def linker(source_folder, target_folder, space):
    """recursively links files to a folder"""

    exceptions = ['.gitignore', '.git', 'linker.py']

    items = list(os.listdir(source_folder))
    items = sorter(items)
    for file in items:
        if file not in exceptions:
            source = os.path.join(source_folder, file)
            target = os.path.join(target_folder, file)

            if '.' not in file:
                print('\n' + space + file)
                os.makedirs(target)
                linker(source, target, space + '  ')

            else:
                print(space + file)
                subprocess.call(['ln', source, target])


if __name__ == '__main__':
    source_folder = os.getcwd()
    target_folder = '/home/doakey/.config/blender/2.79/scripts/addons/'
    target_folder += 'Blender-power-sequencer-master'  # ntpath.basename(source_folder)

    try:
        os.makedirs(target_folder)
    except FileExistsError:
        shutil.rmtree(target_folder)
        os.makedirs(target_folder)

    linker(source_folder, target_folder, '')
