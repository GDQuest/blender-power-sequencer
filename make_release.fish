#!/usr/bin/env fish

set blender_addons_repo $HOME/Repositories/applications/blender-git/blender/release/scripts/addons/
set out_path power_sequencer

function make_release
    rm -v $out_path.zip
    mkdir -v $out_path
    echo "Copying all files and directories to $out_path."
    cp -r (string match -v $out_path -- *) $out_path

    echo "Deleting development files from the release copy."
    cd $out_path
    # Enumerate files for wildcards without matches
    for i in **__pycache__ *.fish img/ **LICENSE **MANIFEST.in **Makefile **pyproject.toml **.md scripts/ShortcutsDocs
        rm -r $i
    end
    cd ..

    echo "Compressing the release directory to a zip archive for the GitHub release."
    zip --quiet $out_path.zip $out_path/**

    echo "Making the blender version."
    sed -i s/blender_power_sequencer/power_sequencer/ $out_path/tools/__init__.py $out_path/operators/__init__.py

    echo "Copying the files to the Blender Addons repository."
    echo "Removing $blender_addons_repo/$out_path."
    rm -r $blender_addons_repo/$out_path
    echo "Copying $out_path to $blender_addons_repo."
    cp -r $out_path $blender_addons_repo

    echo "Deleting the build directory $out_path."
    rm -rf $out_path

    echo "Done. Build with Blender, run `make update && make test`, and test in a development build before pushing."
end

make_release
