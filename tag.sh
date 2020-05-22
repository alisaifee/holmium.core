#!/bin/bash
dryrun=0
while [ "$1" != "" ]; do
    case $1 in
        -d | --dryrun )    dryrun=1
                           ;;
    esac
    shift
done

rm -rf build dist
last_tag=$(git tag | sort -nr | head -n 1)
echo current version:$(python setup.py --version), current tag: $last_tag
read -p "new version:" new_version
last_portion=$(grep -P "^History$" HISTORY.rst -5 | grep -P "^v\d+.\d+.\d+")
changelog_file=/var/tmp/holmium.core.newchangelog
new_changelog_heading=${new_version}
new_changelog_heading_sep=$(python -c "print('='*len('$new_changelog_heading'))")
echo $new_changelog_heading > $changelog_file
echo $new_changelog_heading_sep >> $changelog_file
echo "Release Date: `date +"%Y-%m-%d"`" >> $changelog_file
python -c "print(open('HISTORY.rst').read().replace('$last_portion', open('$changelog_file').read() +'\n' +  '$last_portion'))" > HISTORY.rst.new
cp HISTORY.rst.new HISTORY.rst
vim -O HISTORY.rst <(echo \# vim:filetype=git;git log $last_tag..HEAD --format='* %s (%h)%n%b' | sed -E '/^\*/! s/(.*)/    \1/g')
if rst2html.py HISTORY.rst > /dev/null
then
    echo "tagging $new_version"
    git add HISTORY.rst
    git commit -m "Update changelog for  ${new_version}"
    git tag -s ${new_version} -m "Release version ${new_version}"
    python setup.py build sdist bdist_egg bdist_wheel
    test $dryrun != 1 && twine upload dist/*
    rm HISTORY.rst.new
else
    echo changelog has errors. skipping tag.
fi;


