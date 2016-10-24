Templates and tools for creating lecture slides
===============================================

Getting the manual
------------------

To build the presentation slides with instructions::

    ./build-slides.py title.html template-slides.html plain-slides.html math-slides.html build-slides.html

The open the file ``index.html``.

Building and publishing pages for this repository
-------------------------------------------------

Clone the repository::

    git clone ... lecture-slides-template

Clone again into different directory and switch to ``gh-pages`` branch
in this clone::

    git clone ... lecture-slides-template-pages
    cd lecture-slides-template-pages
    git checkout gh-pages

Navigate to the first clone and build pages::

    cd ../lecture-slides-template
    ./copy-common-files.py --dst-dir=../lecture-slides-template-pages/
    ./build-slides.py --outdir=../lecture-slides-template-pages/ title.html template-slides.html plain-slides.html math-slides.html build-slides.html

Navigate to the other clone to commit and push::

    cd ../lecture-slides-template-pages
    git add -A
    git commit -am "new colors for the website"
    git push

About
-----

Presentation is using on Reveal.js HTML Presentation Framework.

 * http://lab.hakim.se/reveal-js/#/
 * https://github.com/hakimel/reveal.js/
