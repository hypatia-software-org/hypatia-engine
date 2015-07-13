#!/bin/sh
#
# Create sphinx api docs.

# lazily slapped together, will come back to improve
rm -rf build
sphinx-apidoc -f -o . ../hypatia
sphinx-build . build
firefox build/index.html
