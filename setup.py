#!/usr/bin/env python

import sys
from setuptools import setup
from distutils.version import StrictVersion

# figure out python version and bail if we're not >3.6
python_version = StrictVersion('.'.join(str(n) for n in sys.version_info[:3]))
if python_version < StrictVersion('3.6'):
    raise RuntimeError("Hypatia Engine requires at least Python version 3.6.")

exec(open('hypatia/__init__.py').read())

install_requires = [
    'Pillow>=2',
    "pygame",
    "docopt"
]

setup_args = {
    "name": 'hypatia_engine',
    "packages": ['hypatia'],
    "version": __version__,
    "description": '2D action adventure game engine',
    "setup_requires": ['setuptools-markdown'],
    "install_requires": install_requires,
    "long_description_markdown_filename": 'README.md',
    "author": 'Hypatia Software Organization',
    "author_email": 'contact@hypatiasoftware.org',
    "url": 'http://engine.hypatiasoftware.org',
    "download_url": 'https://github.com/hypatia-software-org/hypatia-engine/releases/tag/' + __version__,
    "license": 'MIT',
    "entry_points": {
        "console_scripts": [
            "hypatia = hypatia.__main__:main"
        ],
    },
    "classifiers": [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: Linux',
        'Topic :: Games/Entertainment :: Role-Playing',
        'Topic :: Software Development :: Libraries :: pygame',
    ],
    "keywords": (
        'games gaming development sprites adventure game tilemap '
        'tilesheet zelda gamedev 2d'
    ),
}

setup(**setup_args)

