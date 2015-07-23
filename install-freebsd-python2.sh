#!/bin/sh
#
# Installation script for Python 2 on FreeBSD.
#
# This script uses sudo/root privileges to install the following
# packages through the FreeBSD package manager (pkg):
#   * python27
#   * python27-pip to install Python 2.7 requirements
#   * py27-game because pygame isn't on pypi
#
# After installing the aforementioned, the install-base-python2.sh
# script is ran, which uses pip to install all of the requirements
# for Hypatia/Python 2.

sudo pkg install python27 py27-pip py27-game
./install-base-python2.sh

