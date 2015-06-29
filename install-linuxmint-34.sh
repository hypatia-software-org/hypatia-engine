#!/bin/sh
# Hypatia installation script for Linuxmint and Python 3.4.
#
# Forgot which version this was tested in.

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
pip3 install --user -r requirements.txt .

