#!/bin/sh

# builds pages from source

OUTDIR=../mea582-gh-pages

mkdir -p $OUTDIR

HEAD_FILE=head.html
FOOT_FILE=foot.html


for FILE in `ls *.html|grep -v foot|grep -v head`
do
    cat $HEAD_FILE > $OUTDIR/$FILE
    echo "<!-- This is a generated file. Do not edit. -->" >> $OUTDIR/$FILE
    ./strip-whitestace.py < $FILE >> $OUTDIR/$FILE
    cat $FOOT_FILE >> $OUTDIR/$FILE
done

for FILE in *.css
do
    cp --update $FILE $OUTDIR
done

for DIR in img
do
    cp --update --recursive $DIR $OUTDIR
done
