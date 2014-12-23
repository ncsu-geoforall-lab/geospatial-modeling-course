#!/bin/bash

if [ $$ -eq 0 ]; then
    echo "Usage:" 1>&2;
    echo "    $0 file [file...]" 1>&2;
    exit
fi

for file in "$@"
do
    links=$(linkchecker --no-status --output=blacklist --recursion-level=1 $file)
    if [ $? -ne 0 ]; then
        if [ "$links" ]; then
            echo "Invalid links for file $file:"
            echo "$links" | sed "s|file://$(pwd)/||g"
        else
            echo "There might be something wrong with links in $file file. Use linkchecker directly to see the errors or warnings."
        fi
    fi
done
