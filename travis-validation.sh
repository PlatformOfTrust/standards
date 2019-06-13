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
    exit 1
fi
