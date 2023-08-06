#!/bin/bash


# Script to release FlexMeasures to Pypi
#
# The version comes from setuptools_scm. See `python setup.py --version`.
# It includes a .devXX identifier, where XX is the number of commits since the last version tag.
# We disable its ability to add a local scheme (git commit and date) as well, as that
# isn't formattet in a way that pypi accepts it.
# You can instead add a number if you need to release multiple dev versions per commit.

read -p "Are you sure you don't have a config file within these folders (which might get sent along)? [yN] " -n 1 -r
echo    # move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Exiting ..."
    exit 1
fi
echo "Alright, then ..."

rm -rf build/* dist/*

pip -q install twine

python setup.py egg_info sdist
python setup.py egg_info bdist_wheel

twine upload --verbose dist/*
exit


# TODO: if ".dev" in version, then make a dev build
#       (with everything after .dev input for --tag-build)
#       So we remove the $1 and $2 parameters.
#       It could be that pypi will reject that (not only letter,
#       so maybe we can filter those out)

if [ "$1" = "dev" ]; then
    if [ "$2" != "" ]; then
        dev_number=$2
        cleandevtag=${dev_number//[^0-9]/}  # only numbers
        if [ "$cleandevtag" != "$dev_number" ]; then
            echo "Only numbers in the dev tag please! (leave out x.y.z.dev)"
            exit 2
        fi
    else
        echo "Looking up the number of revisions to use as dev release identifier ... "
        dev_number=`git log --oneline | wc -l`
    fi
    
    echo "Using $dev_number as dev build number ..."

    python setup.py -q alias dev egg_info --tag-build=.dev$dev_number
    python setup.py dev sdist
    python setup.py dev bdist_wheel
elif [ "$1" = "release" ]; then
    python setup.py -q alias release egg_info -Db ""
    python setup.py release sdist
    python setup.py release bdist_wheel
else
    echo "Argument needs to be release or dev"
    exit 2
fi

twine upload --verbose dist/*
