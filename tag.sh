#!/bin/bash 
echo current version:$(python -c "import rieapie;print rieapie.version")
read -p "new version:" new_version
sed -i -e "s/version.*/version=\"${new_version}\"/g" rieapie/__init__.py 
git add rieapie/__init__.py 
git commit -m "updating version to ${new_version}"
git tag -s $(python setup.py --version) -m "tagging version ${new_version}"
python setup.py build sdist bdist_egg upload
