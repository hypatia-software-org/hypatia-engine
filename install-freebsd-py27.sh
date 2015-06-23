# Hypatia installation script for FreeBSD.
#
# Tested on FreeBSD 10.1-RELEASE-p10.
#
# Performs the following tasks:
#   1. Installs the following FreeBSD packages: python27, py27-pip,
#      and py27-game; as root.
#   2. Installs Python package requirements through PIP as normal user.
#   3. Installs the Hypatia package as normal user.


sudo pkg install python27 py27-pip py27-game
pip install --user -r requirements.txt .

