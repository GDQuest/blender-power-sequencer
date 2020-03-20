#!/usr/bin/env fish

set blender_addons_repo $HOME/Repositories/applications/blender-git/blender/release/scripts/addons/

function make_release
    set out_path "power_sequencer"

    rm -v $out_path.zip
    mkdir -v $out_path && cp -rv (string match -v $out_path -- *) $out_path

    echo "Deleting development files from the release copy."
    cd $out_path
    # Enumerate files for wildcards without matches
    for i in **__pycache__ **TAGS **GPATH **GRTAGS **GTAGS *.fish img/ **LICENSE **MANIFEST.in **Makefile **pyproject.toml **.md scripts/ShortcutsDocs
        rm -rv $i
    end
    cd ..

    echo "Compressing the release directory to a zip archive."
    zip $out_path.zip $out_path/**

    echo Copying the files to the blender addons repository
    rm -r $blender_addons_repo/$out_path
    cp -r $out_path $blender_addons_repo

    echo "Deleting the release copy directory."
    rm -rfv $out_path

    echo "Done. Build with Blender, run `make test`, and test in a development build before pushing."
end

make_release
