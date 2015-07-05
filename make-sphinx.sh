#!/bin/sh
#
# Create sphinx api docs.

# lazily slapped together, will come back to improve
test.sh
rm -rf api
sphinx-apidoc -f -o sphinx-source/ hypatia
sphinx-build sphinx-source api
firefox api/index.html
