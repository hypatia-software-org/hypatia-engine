#!/bin/sh
#
# Hypatia installation script for Linuxmint.
#
# Performs the following tasks:
#   1. Installs the packages python-pygame
#   2. Installs Python package requirements through PIP as normal user.
#   3. Installs the Hypatia package as normal user.
#
# This script requires sudo/root privileges in order to install
# the pygame package, since it doesn't have a package on PyPi.

sudo apt-get install python-pygame
./install-base-python2.sh
