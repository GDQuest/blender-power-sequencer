#!/usr/bin/ fish
set directory "power_sequencer"
rm -rf $directory
rm $directory.zip
mkdir $directory
cp * -r $directory
rm -r $directory/**__pycache__ $directory/power-sequencer_updater $directory/**GPATH $directory/**GRTAGS $directory/**GTAGS $directory/*.fish $directory/img/ $directory/$directory $directory/LICENSE $directory/pyproject.toml $directory/**.md
zip $directory.zip $directory/**
rm -rf $directory
