NCSU GIS/MEA582: Geospatial Modeling and Analysis
=================================================


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
use `build-pages.sh` script to build the pages.

    ./build-pages.sh

The directory where pages are build is on the same level as directory with
the source code and is named `mea582-gh-pages`.
You can look at the pages using e.g.

    firefox ../mea582-gh-pages/index.html

If you don't see the changes you have made, delete the file in the build
directory and build again (the mechanism to recognize changes is not smart).


### Publishing the pages

One should not forget to commit and push changes to the repository
when publishing so that changes are shared with other contributors.
This is ensured using a script `build-and-publish.sh`.
The script will require you to have all all changes committed and pushed
and then it will publish them.

The script requires one parameter which is a destination for the `rsync`
command. To work more effectively, you can create a script
named `my-build-and-publish.sh` with hard-coded destination,
for example:

    #!/bin/bash

    ./build-and-publish.sh john@university.edu:/courses/gis/

Don't forget to set it executable using `chmod u+x`.
If you name the script `my-build-and-publish.sh`, it will be ignored by Git
and you can publish the pages using:

    ./my-build-and-publish.sh


New semester checklist
----------------------

A list of what should be changed, updated or checked for new semester
in the web pages.

* change dates in the schedule
* update students' Google Site name template
* update course Google Site URL
* create a new page for project titles and link it


License
-------

The text and images in this repository are under CC BY-SA 4.0 license.

Note that a lot of things are just linked material or data from different
sources which can have different licenses.

The license does not apply to logos included in the web pages.
