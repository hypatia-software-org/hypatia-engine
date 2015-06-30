#!/bin/sh
# Hypatia installation script for Linuxmint.
#
# Forgot which version this was tested in.
#
# Performs the following tasks:
#   1. Installs the packages python-pygame
#   2. Installs Python package requirements through PIP as normal user.
#   3. Installs the Hypatia package as normal user.


sudo apt-get install python-pygame
pip install --user -r requirements.txt .

