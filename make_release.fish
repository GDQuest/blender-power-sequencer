#!/usr/bin/ fish
set directory "power_sequencer"
rm -rf $directory
rm $directory.zip
mkdir $directory
cp * -r $directory
for i in $directory/**__pycache__ $directory/power-sequencer_updater $directory/**GPATH $directory/**GRTAGS $directory/**GTAGS $directory/*.fish $directory/img/ $directory/$directory $directory/**LICENSE $directory/**MANIFEST.in $directory/**Makefile $directory/**pyproject.toml $directory/**.md $directory/scripts/ShortcutsDocs
    rm $i -r
end
zip $directory.zip $directory/**
rm -rf $directory
