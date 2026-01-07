NCSU GIS/MEA582: Geospatial Modeling and Analysis
=================================================

[![Publish the website](https://github.com/ncsu-geoforall-lab/geospatial-modeling-course/workflows/Publish%20the%20website/badge.svg)](https://github.com/ncsu-geoforall-lab/geospatial-modeling-course/actions?query=workflow%3A%22Publish+the+website%22)

Authors
-------

Copyright 2008-2024 by

 * Helena Mitasova
 * Rob Austin
 * Anna Petrasova
 * Vaclav Petras
 * Paul Paris
 * Corey White

Course developed at North Carolina State University,
Center for Geospatial Analytics and
Department of Marine, Earth, and Atmospheric Sciences.

See the license below.

Online version of the materials
-------------------------------

The (static) website for this course is using GitHub pages and the URL is:

* https://ncsu-geoforall-lab.github.io/geospatial-modeling-course

Old URLs (for archival purposes):

    https://ncsu-osgeorel.github.io/geospatial-modeling-course
    https://courses.ncsu.edu/gis582/common
    https://courses.ncsu.edu/mea582/common/GIST.html


Basic Git introduction
----------------------

Clone this repository using `git clone` and the URL from the green button
near the top of the page (this is a Git alternative to downloading a ZIP file).

Change directory (using `cd`) into the newly created directory.

Once you edit some files, use `git commit` to commit them. Use `-a` flag to
commit all or specify the filenames to commit just some of them.
Use `-m "some commit message"` to describe the changes you made.
The fastest way to commit might be, for example:

    git commit -am "updated for GRASS 8.4.2"

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
code and placed into a separate directory. The publishing step
is done using a script which makes GitHub pages publishing
even easier than it already is.


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

To build lectures go to the lecture directory and run the `build.sh`
for lectures script there, i.e.:

    cd lectures
    ./build.sh

It is important to always be in the directory where the `build.sh`
script is for each part.

### Publishing the pages

Once the changed and committed and pushed to the main branch, the
website will be deployed automatically using GitHub Actions.


New semester checklist
----------------------

A list of what should be changed, updated or checked for new semester
in the web pages.

* change dates in the schedule (in this repository)
* update links to the Moodle site
* create a new page for project titles and link it
* search for all other occurrences of string `term-changes` and update
* update to current GRASS release
* email students with link to the website and to Moodle

The `term-changes` should be added to all places which needs to be
changed each semester (term). To HTML it should be added as a class.
All occurrences can be found using:

```
grep -IrnE term-changes --exclude=README.md --exclude-dir={build,.git}
```

### New calendar year changes

Change the copyright years in this readme and in `foot.html`.
Confirm with:

```
grep -Irn "[^0-9]old_year_here[^0-9]"
```

### Updating for new GRASS releases

Update commands URLs for documentation:

```
grep -IrnE grassXY --exclude=README.md --exclude-dir={build,.git}
./replace_string.sh grassXY grassXZ
```

Now run the *grep* command again, to get what the script does not
handle.

Find also other locations where a specific GRASS version is
mentioned (replace `X` and `Y` with version number):

```
grep -IrnE "[^0-9]X\.Y[^0-9]" --exclude=README.md --exclude-dir={build,.git}
```

Testing GRASS assignments
-----------------------------

Prepare new directory and mapset:

```
mkdir test
cd test
ln -s ../grass/data data
grass -c -e ~/grassdata/nc_spm_08_grass7/test/
```

For each assignment:

```
../doc2tests.py < ../grass/buffers_cost.html > test.sh
chmod u+x test.sh
grass ~/grassdata/nc_spm_08_grass7/test/ --exec ./test.sh
```

Now, inspect the output and files in the directory.

Then delete the created maps and images.

```
grass ~/grassdata/nc_spm_08_grass7/test/ --exec g.remove type=raster,vector patter="*" -f
rm *.png
```

After all tests, remove the directory and the mapset:

```
cd ..
rm -r test
rm -r ~/grassdata/nc_spm_08_grass7/test/
```

Automatic indexes
-----------------

Topics index and GRASS assignments index are generated automatically.
The process is split into two phases. First, links to pages are extracted
from a given page. This introduces the desired order of the linked pages
(alternative would be, e.g. alphabetical order based on file names
and directory listing). In the second phase, individual files are search
for the main heading and optionally subheadings. These headings
are used to create the text in the index page.
See `extract-links.py`, `generate-index.py` and `build.sh` for details.

Subtopics are extracted from the topics pages when they have `class="subtopic"`.


License
-------

The text and images in this repository are under CC BY-SA 4.0 license.

Note that a lot of things are just linked material or data from different
sources which can have different licenses.

The license does not apply to logos included in the web pages.
