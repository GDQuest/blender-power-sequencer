#!/usr/bin/env fish
# Generates

set -l target_directory $HOME/Repositories/website/data/blender
set -l json_file power_sequencer_docs.json

if not test -d $target_directory
    echo The target directory $target_directory does not exist.
    echo Canceling the operation.
    exit 1
end

echo Regenerating the JSON data file for the docs
blender --background --factory-startup -noaudio --python ./scripts/ShortcutsDocs/shortcuts_docs.py
mv -v $json_file $target_directory
