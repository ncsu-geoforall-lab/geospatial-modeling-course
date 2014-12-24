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


Basic Git introduction
----------------------

Create a directory `mea582_all` or something like that and cd into it. Clone the repository:

    git clone git@github.ncsu.edu:osgeorel/mea582.git

Eventually, you will have two directories at this directory level,
one with the source code and another with the build of the pages.

Do all the changes in the `mea582` directory created by the `git clone` command.

Once you edit some files, use `git commit` to commit them. Use `-a` flag to
commit all or specify the filenames to commit just some of them.
Use `-m "some commit message"` to describe the changes you made.
The fastest way to commit might be, for example:

    git commit -am "updated for GRASS GIS 7"

If you want to provide a longer commit message, just omit the `-m "..."` and
you will get an editor (`nano` by default) where you can write a commit message.

If you created a new file, you have to tell Git to start tracking it:

    git add some_file.txt

If you want to delete or move files, use `git rm` and `git mv`.

To see what files where changed, added or deleted use `git status`.

To review the changes in the files use `git diff`.

The commit itself records the change locally but does not put the change
to the remote repository.
Once you are ready to share your changes with others use `git push`
to put the changes to the remote repository.
All commits which were not pushed yet will by pushed.

To get the changes of other contributors use `git pull`.
You always have to pull before you push. It is often necessary to commit
your changes before `git pull` otherwise Git will not be able to merge
the incoming changes. If you get an editor with a message about merging,
it is enough just to use the generated message by exiting the editor
(using Ctrl+X in case the editor is `nano`).
If the automatic merge is not possible, Git will put the conflicting parts
into the files and mark them. Consult the further steps with other contributors.


Build and publish
-----------------

Web page is published using GitHub pages. The pages are build from the source
code into a directory which is a clone of a repository with gh-pages branch
active. The publishing step is done using Git.


### Creating a directory for publishing

These steps are done just once by each contributor who wants to publish
the pages online.

Using the following command create a new clone of the repository.
The clone will be named `mea582-gh-pages`.
You should and place it at the same level where you have the repository clone
where you work with master branch.

    git clone git@github.ncsu.edu:osgeorel/mea582.git mea582-gh-pages

Checkout (switch to) `gh-pages` branch:

    cd mea582-gh-pages
    git checkout gh-pages

Now you are ready to to build a publish pages. Your directory tree should look
like:

    some_directory (directory of your choice)
        - mea582 (the directory with source code, master branch)
        - mea582-gh-pages (the directory for build and publishing, gh-pages branch)


### Building the pages

In your clone of the repository where you are in master branch,
use `build-pages.sh` script to build the pages.

    ./build-pages.sh

You can look at them using e.g.

    firefox ../mea582-gh-pages/index.html

If you don't see the changes you have made, delete the file in the build
directory and build again (the mechanism to recognize changes is not smart).


### Publishing the pages

It is necessary to commit and push changes in `mea582-gh-pages` repository clone
to publish them. One should not forget to commit and push changes also
in the master branch repository.
This is ensured using a script `build-and-publish.sh`:

    ./build-and-publish.sh

The script will require you to have all all changes committed and pushed
and then it will publish them.


### Creating a gh-pages branch

This is done only once at the beginning by the contributor who is creating
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

You can read more about it in GitHub documentation:

* https://help.github.com/articles/creating-project-pages-manually/


License
-------

The text and images in this repository are under CC BY-SA 4.0 license.

Note that a lot of things are just linked material or data from different
sources which can have different licenses.
