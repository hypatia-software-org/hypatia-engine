#!/bin/sh
#
# This script is STRONGLY recommended for verifying the quality and
# functionality of your contribution.
#
# This script can be ran as a pre-push git hook; please see the etc/
# directory in this project's root.
#
# Not used for Travis CI, because this launches the demo game.
#
# Also checks the validity of the markdown-to-PyPI-rst conversion
# performed on README.md. This is done in order to provide PyPi
# with a nice package page/read me.
#
# CAVEAT: If you get an error about --no-cache-dir,
# you need to upgrade pip.
#
# This script does the following:
#   1. Uninstall the current hypatia_engine Python package
#   2. convert README.md to PKG-INFO (rst)
#   3. Validate PKG-INFO, if it doesn't validate it won't be
#      formatted on PyPi
#   4. Install the local repo's package for Hypatia as user,
#      using pip and setup.py.
#   5. Remove the PKG-INFO file (we were only validating it)
#   6. Use py.test to check for PEP8 rule violations, to
#      doctest all docstrings, provide a test coverage
#      report and pipe all of this information to MORE
#   7. The demo game.py will be launched, utilizing the
#      freshly installed Hypatia package from this local
#      repository.

pip uninstall hypatia_engine -y
pandoc README.md -t rst -o PKG-INFO
python setup.py check -r -s
pip install --user --no-cache-dir .
rm PKG-INFO
py.test tests --pep8 --doctest-modules hypatia -v --cov-report term-missing --cov=hypatia | more
cd demo
python game.py
cd ..
