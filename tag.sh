#!/bin/bash 
echo current version:$(python -c "import holmium.version;print holmium.version.__version__")
read -p "new version:" new_version
sed -i -e "s/__version__.*/__version__=\"${new_version}\"/g" holmium/version.py 
git add holmium/version.py
git commit -m "updating version to ${new_version}"
last_portion=$(grep -E "^History$" HISTORY.rst -5 | grep -E "^\d+.\d+.\d+")
changelog_file=/var/tmp/holmium.core.newchangelog
new_changelog_heading="${new_version} `date +"%Y-%m-%d"`"
new_changelog_heading_sep=$(python -c "print '='*len('$new_changelog_heading')")
echo $new_changelog_heading > $changelog_file
echo $new_changelog_heading_sep >> $changelog_file
python -c "print open('HISTORY.rst').read().replace('$last_portion', open('$changelog_file').read() +'\n' +  '$last_portion')" > HISTORY.rst.new 
cp HISTORY.rst.new HISTORY.rst 
vim HISTORY.rst
if rst2html.py HISTORY.rst > /dev/null 
then
    echo "tagging $new_version"
    git add HISTORY.rst 
    git tag -s $(python setup.py --version) -m "tagging version ${new_version}"
    python setup.py build sdist bdist_egg upload
else
    echo changelog has errors. skipping tag. 
fi;


