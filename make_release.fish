#!/usr/bin/env fish

function make_release
    set out_path "power_sequencer"

    echo "Deleting the previous release archive."
    rm $out_path.zip

    echo "Copying the add-on files and development files to the" $out_path "directory".
    mkdir $out_path && cp -r (string match -v $out_path -- *) $out_path

    echo "Deleting development files from the release copy."
    cd $out_path
    # Enumerate files for wildcards without matches
    for i in **__pycache__ **TAGS **GPATH **GRTAGS **GTAGS *.fish img/ **LICENSE **MANIFEST.in **Makefile **pyproject.toml **.md scripts/ShortcutsDocs
        rm -r $i
    end
    cd ..

    echo "Compressing the release directory to a zip archive."
    zip $out_path.zip $out_path/**
    echo "Deleting the release copy directory."
    rm -rf $out_path
end

make_release
