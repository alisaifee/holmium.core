#!/bin/bash 
echo current version:$(python -c "import holmium.core;print holmium.core.__version__")
read -p "new version:" new_version
sed -i -e "s/__version__.*/__version__=\"${new_version}\"/g" holmium.core/__init__.py 
git add holmium/core/__init__.py
git commit -m "updating version to ${new_version}"
git tag -s $(python setup.py --version) -m "tagging version ${new_version}"
python setup.py build sdist bdist_egg upload


