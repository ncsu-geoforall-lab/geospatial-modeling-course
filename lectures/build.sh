BUILD_DIR=../build/lectures

mkdir -p $BUILD_DIR

./copy-common-files.py --dst-dir=$BUILD_DIR

for FILE in `ls *.html|grep -v foot|grep -v head`
do
    ./build-slides.py --outdir=$BUILD_DIR \
        --outfile=$FILE $FILE
done
