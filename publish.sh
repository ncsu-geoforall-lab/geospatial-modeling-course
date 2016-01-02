#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage:" 1>&2;
    echo "    $0 destination" 1>&2;
    exit
fi

output=$(git status --porcelain)
if [ $? -ne 0 ]; then
    echo "git status failed. Are you in a repository?" 1>&2;
    exit
elif [ -n "$output" ]; then
    echo "Cannot publish. There are some untracked files." 1>&2;
    echo "Using \"git status\" to show what is not committed or tracked."
    git status
    exit
fi

current_branch=$(git rev-parse --abbrev-ref HEAD)
if [ $? -ne 0 ]; then
    # there is no point in asking about repository now
    echo "git rev-parse failed. Are you in a repository?" 1>&2;
    exit
elif [ "master" != "$current_branch" ]; then
    echo "You are not on master branch, so you should not build into gh-pages branch." 1>&2;
    echo "Using \"git branch\" to show current branches."
    git branch
    exit
fi


output=$(git log origin/master..master)
if [ $? -ne 0 ]; then
    echo "git log failed. Are you in a repository?" 1>&2;
    exit
elif [ -n "$output" ]; then
    echo "There are some commits which should be pushed before publishing pages." 1>&2;
    echo "Use \"git log origin/master..master\" to review them and \"git push\" to push them to remote repository." 1>&2;
    exit
fi

# the actual build
echo "Building..."
./build.sh

if [ $? -ne 0 ]; then
    echo "Build failed. Use ./build.sh script to debug the issue." 1>&2;
    exit
fi

last_commit=$(git log -n 1  --pretty=format:"%h \"%s\"")

build_dir="../mea582-gh-pages"

cd $build_dir

if [ $? -ne 0 ]; then
    echo "Do you have clone of the repository for gh-pages branch in $build_dir?" 1>&2;
    exit
fi

# the publishing process using rsync

# fail on first error
set -e

echo "You may be asked for password for the server (destination) now."
rsync -rtvu --exclude '.*' * $1

set +e
