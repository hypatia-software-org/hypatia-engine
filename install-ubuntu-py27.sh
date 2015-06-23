# Hypatia installation script for Ubuntu.
#
# Not tested. This doesn't force Python 2.7, I don't think?
#
# Performs the following tasks:
#   1. Installs the Ubuntu packages python-pygame and python-pip.
#   2. Installs Python package requirements through PIP as normal user.
#   3. Installs the Hypatia package as normal user.


sudo apt-get install python-pygame python-pip
pip install --user -r requirements.txt .

