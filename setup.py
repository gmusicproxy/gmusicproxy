#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages
import sys
import os

GMUSICPROXYFILE = 'GMusicProxy'
version_line = open(GMUSICPROXYFILE).read()
version_re = r"programVersion = ['\"]([^'\"]*)['\"]"
match = re.search(version_re, version_line, re.M)
if match:
    version = match.group(1)
else:
    raise RuntimeError("Could not find version in '%s'" % GMUSICPROXYFILE)

setup(
    name='gmusicproxy',
    version=version,
    author='Mario Di Raimondo',
    author_email='mario.diraimondo@gmail.com',
    url='https://github.com/diraimondo/gmusicproxy',
    scripts=[GMUSICPROXYFILE],
    license=open('LICENSE').read(),
    description='Google Play Music Proxy - "Let\'s stream Google Play Music using any music program"',
    long_description=(open('README.md').read()),
    install_requires=['gmusicapi==10.1.0', 'netifaces>=0.10.4',
                      'pyxdg>=0.25', 'eyed3>=0.7.8', 'python-daemon>=2.0.5' if not os.name == 'nt' else ''],
    extras_require={'keyring': 'keyring>=10.0'}
)
