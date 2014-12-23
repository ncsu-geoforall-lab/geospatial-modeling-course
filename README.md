MEA582: Geospatial Modeling and Analysis
========================================

Authors
-------

Copyright 2008-2014 by

 * Helena Mitasova
 * Paul Paris
 * Anna Petrasova
 * Vaclav Petras

Course developed at North Carolina State University.

Build and publish
-----------------

Web page is published using GitHub pages as described at:

* https://help.github.com/articles/creating-project-pages-manually/

### Creating a directory for publishing

Create a new clone of the repository. Name the directory `mea582-gh-pages`
and place it at the same level where you have the repository clone
where you work with master branch.

    git clone git@github.ncsu.edu:osgeorel/mea582.git mea582-gh-pages

Checkout `gh-pages` branch:

    cd grass-intro-workshop-gh-pages
    git checkout gh-pages

### Building the pages

In your clone of the repository where you are in master branch,
use `build-pages.sh` script to build the pages.

    ./build-pages.sh

You can look at them using e.g.:

    firefox ../mea582-gh-pages/index.html

It is necessary to commit and push changes in `mea582-gh-pages` repository clone
to publish them. One should not forget to commit and push changes also
in the master branch repository.
This is ensured using a script `build-and-publish.sh`:

    ./build-and-publish.sh

The script will require you to have all all changes committed and pushed
and then it will publish them.

### Creating a gh-pages branch

This is done only once at the beginning by the one who is creating
the branch for publishing GitHub pages.

Create a new clone at the same directory as the main repository:

    git clone git@github.ncsu.edu:osgeorel/mea582.git mea582-gh-pages
    cd mea582-gh-pages

Create `gh-pages` branch with no parents:

    git checkout --orphan gh-pages

Remove all files from the directory (except for `.git` directory)

    git rm -rf .

Upstream must be defined to be able to pull:

    git branch --set-upstream-to=origin/gh-pages gh-pages

Use the following for the first push:

    git push origin gh-pages

License
-------

The text and images in this repository are under CC BY-SA 4.0 license.

Note that a lot of things are just linked material or data from different
sources which can have different licenses.
