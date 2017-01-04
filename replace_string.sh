#!/bin/bash

if [[ $# -ne 2 ]]
  then
    >&2 echo "Usage:"
    >&2 echo "  $0 old new"
    exit 1
fi

output=$(git status --porcelain)
if [ $? -ne 0 ]; then
    echo "git status failed. Are you in a repository?" 1>&2;
    exit
elif [ -n "$output" ]; then
    echo "No replacement done." 1>&2;
    echo "Replace would be hard to revert because of uncommitted changes." 1>&2;
    echo "Using \"git status\" to show what is not committed or tracked." 1>&2;
    git status
    exit
fi

find . -type f -name "*.html" ! -path ".git/*" ! -path "build" -exec \
    sed -i "s+$1+$2+g" {} +
