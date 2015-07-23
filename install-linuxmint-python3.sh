#!/bin/sh
#
# Hypatia installation script for Linuxmint and Python 3.4.
#
# Deep wizardry. This is pretty experimental. Use at your
# own risk!
#
# This script installs all of the specific versions of various
# libraries required to support pygame/python3. Then it clones
# the pygame repo from bitbucket, builds pygame with python 3,
# and finally uses pip (for python 3) to install the base
# requirements file and the Hypatia package as a regular user.

# install depends
sudo apt-get install python3-pip python3-dev libsdl1.2-dev\
     libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev\
     libsdl-gfx1.2-dev libsdl-net1.2-dev libsdl-image1.2-dev\
     libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev\
     libsdl1.2-dev libportmidi-dev libswscale-dev libavformat-dev\
     libavcodec-dev libsdl-sge-dev libsdl-sound1.2-dev\
     libportmidi-dev libsmpeg-dev

# compile pygame
hg clone https://bitbucket.org/pygame/pygame
cd pygame
python3 setup.py build
cd ..
pip3 install --user -r requirements/base.txt .
