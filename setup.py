#!/usr/bin/env python

from distutils.core import setup

exec(open('hypatia/version.py').read())
setup(name='hypatia',
      version=__version__,
      description='2D adventure game engine',
      author='Lillian Lemmer',
      author_email='lillian.lynn.lemmer@gmail.com',
      #url='http://www.python.org/sigs/distutils-sig/',
      packages=['hypatia'],
    )
