BUILD_DIR=../build/lectures

mkdir -p $BUILD_DIR

./copy-common-files.py --dst-dir=$BUILD_DIR

./build-slides.py --outdir=$BUILD_DIR \
    --outfile=about.html \
    about.html
