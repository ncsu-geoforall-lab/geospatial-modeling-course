#!/bin/sh

# builds pages from source

OUTDIR=../mea582-gh-pages

if [ ! -d "$OUTDIR" ]; then
    echo "The directory $OUTDIR does not exists and it will be created for you."
    echo "This is fine if you want to just view the pages."
    echo "However, if you want to publish the web pages, you should delete it and follow the instructions in README."
    mkdir $OUTDIR
fi

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
        ./increase-link-depth.py < $HEAD_FILE > $TGT_FILE
        echo "<!-- This is a generated file. Do not edit. -->" >> $TGT_FILE
        ./strip-whitestace.py < $FILE >> $TGT_FILE
        ./increase-link-depth.py < $FOOT_FILE >> $TGT_FILE
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
