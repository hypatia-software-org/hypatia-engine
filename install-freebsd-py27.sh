#!/bin/sh
# Hypatia installation script for FreeBSD.
#
# Tested on FreeBSD 10.1-RELEASE-p10. ZSH.


sudo pkg install python27 py27-pip py27-game
pip install --user -r requirements/base.txt
pip install --user -r requirements/python2.txt .

