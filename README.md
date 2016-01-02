NCSU GIS/MEA582: Geospatial Modeling and Analysis
=================================================


Authors
-------

Copyright 2008-2015 by

 * Helena Mitasova
 * Rob Austin
 * Anna Petrasova
 * Vaclav Petras
 * Paul Paris

Course developed at North Carolina State University.


Online version of the materials
-------------------------------

The (static) website for this course is using GitHub pages and the URL is:

* http://ncsu-osgeorel.github.io/geospatial-modeling-course

Old URLs (for archival purposes):

* http://courses.ncsu.edu/gis582/common/
* https://courses.ncsu.edu/mea582/common/GIST.html


Basic Git introduction
----------------------

Create a directory `mea582_all` or something like that and `cd` into it.
Clone the repository:

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

Web page is published NCSU course web space. The pages are build from the source
code into a separate directory. The publishing step is done using a script.


### Building the pages

In your clone of the repository where you are in master branch,
use `build.sh` script to build the pages.

    ./build.sh

The directory where pages are build is inside the directory with
the source code and is named `build`.
You can look at the pages using e.g.

    firefox build/index.html

If you don't see the changes you have made, delete the file in the build
directory and build again (the mechanism to recognize changes is not smart).


### Publishing the pages

One should not forget to commit and push changes to the repository
when publishing so that changes are shared with other contributors.
This is ensured using a script `publish.sh`.
The script will require you to have all all changes committed and pushed
and then it will publish them.


New semester checklist
----------------------

A list of what should be changed, updated or checked for new semester
in the web pages.

* change dates in the schedule
* update students' Google Site name template
* update course Google Site URL
* create a new page for project titles and link it
* emails to share Google Site with and send the homeworks to


License
-------

The text and images in this repository are under CC BY-SA 4.0 license.

Note that a lot of things are just linked material or data from different
sources which can have different licenses.

The license does not apply to logos included in the web pages.
