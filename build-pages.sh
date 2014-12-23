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

for DIR in grass arcgis resources project_titles
do
    mkdir -p $OUTDIR/$DIR

    for FILE in `ls $DIR/*.html`
    do
        TGT_FILE=$OUTDIR/$DIR/`basename $FILE`
        ./increase-file-depth.py < $HEAD_FILE > $TGT_FILE
        echo "<!-- This is a generated file. Do not edit. -->" >> $TGT_FILE
        ./strip-whitestace.py < $FILE >> $TGT_FILE
        ./increase-file-depth.py < $FOOT_FILE >> $TGT_FILE
    done
done

for FILE in *.css
do
    cp --update $FILE $OUTDIR
done

for DIR in img
do
    cp --update --recursive $DIR $OUTDIR
done
