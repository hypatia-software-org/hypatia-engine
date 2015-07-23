#!/bin/sh
#
# Any commands which can be used to install dependencies across ALL
# supported BSD and Linux (maybe even Mac?) platforms.
#
# This script is used by other python2 install scripts.

pip install --user -r requirements/python2.txt .

