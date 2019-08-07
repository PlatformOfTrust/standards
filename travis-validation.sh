#!/usr/bin/env sh
set -exu

FOUND_FILES=`find . -name "*.sh" -not -executable`
if [ -z "$FOUND_FILES" ]; then
    echo "All files have -x applied."
else
    echo "Files that don't have -x applied:"
    for i in $FOUND_FILES; do
        echo " * $i"
    done

    echo 'In order to fix this please execute the following in the repo root:'
    echo 'git update-index --chmod=+x <filename>'
    echo 'git commit -m "Made scripts executable"'
    echo 'git push'

    exit 1
fi
