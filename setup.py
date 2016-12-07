#!/usr/bin/env python

"""Hypatia package installer.

Distributing:

  $ setup.py sdist bdist_wheel
  $ twine upload dist/hypatia_engine-0.2.3.tar.gz dist/hypatia_engine-0.2.3*.whl
  $ rm -rf dist

  You'll need the wheel, twine package for bdist_wheel. Don't forget
  to clear your dist when finished.

Installing:
  `pip install .` in the project root. This script detects the
  python version and builds the install_requires accordingly.

  Does not install pygame. See `README.md`.

"""

import sys
from setuptools import setup
from distutils.version import StrictVersion

install_requires = ['Pillow>=2']

exec(open('hypatia/__init__.py').read())
setup(name='hypatia_engine',
      packages=['hypatia'],
      version=__version__,
      description='2D action adventure game engine',
      setup_requires=['setuptools-markdown'],
      # pygame isn't on pypi
      # TODO: i should maybe also specifiy Pillow<4
      install_requires=install_requires,
      long_description_markdown_filename='README.md',
      author='Hypatia Software Organization',
      author_email='contact@hypatiasoftware.org',
      url='http://engine.hypatiasoftware.org',
      download_url = 'https://github.com/hypatia-software-org/hypatia-engine/releases/tag/' + __version__,
      license='MIT',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.5',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX :: BSD :: FreeBSD',
                   'Operating System :: POSIX :: Linux',
                   'Topic :: Games/Entertainment :: Role-Playing',
                   'Topic :: Software Development :: Libraries :: pygame',
                  ],
      keywords=('games gaming development sprites adventure game tilemap '
                'tilesheet zelda gamedev 2d')
    )

