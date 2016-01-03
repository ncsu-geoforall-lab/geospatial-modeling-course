remote=$(git config --get remote.origin.url)

build_dir="build"

rm -r $build_dir

git clone $remote $build_dir

cd $build_dir

git checkout gh-pages
