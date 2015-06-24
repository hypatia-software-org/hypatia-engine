#!/usr/bin/env python

"""Hypatia package installer.

Notes:
  $ python setup.py sdist bdist_wheel upload

"""

from distutils.core import setup


exec(open('hypatia/version.py').read())
setup(name='hypatia',
      version=__version__,
      description='2D adventure game engine',
      author='Lillian Lemmer',
      author_email='lillian.lynn.lemmer@gmail.com',
      url='http://lillian-lemmer.github.io/hypatia',
      license='MIT',
      packages=['hypatia'],
      install_requires=['pygame', 'pillow', 'pyganim'],
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4',
                   'Operating System :: Microsoft :: Windows :: Windows 7',
                   'Operating System :: Microsoft :: Windows :: Windows Vista',
                   'Operating System :: Microsoft :: Windows :: Windows XP',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX :: BSD :: FreeBSD',
                   'Operating System :: POSIX :: Linux',
                   'Topic :: Games/Entertainment :: Role-Playing',
                   'Topic :: Software Development :: Libraries :: pygame',
                  ],
      keywords=('games gaming development sprites adventure game tilemap '
                'tilesheet zelda gamedev 2d')
    )

