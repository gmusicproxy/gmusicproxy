#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages
import sys
import os
import json

GMUSICPROXYFILE = 'GMusicProxy'
with open("version.json") as f:
        match = json.load(f)
if match:
    version = match["version"]
else:
    raise RuntimeError("Could not find version in '%s'" % GMUSICPROXYFILE)

setup(
    name='gmusicproxy',
    version=version,
    author='Mario Di Raimondo et al',
    author_email='gmusicproxy@gmail.com',
    url='https://github.com/gmusicproxy/gmusicproxy',
    scripts=[GMUSICPROXYFILE, "version.json", "gmusicproxyutils.py"],
    license=open('LICENSE').read(),
    description='Google Play Music Proxy - "Let\'s stream Google Play Music using any music program"',
    long_description=(open('README.md').read()),
    install_requires=['gmusicapi==13.0.0', 'netifaces>=0.10.4',
                      'pyxdg>=0.25', 'eyed3>=0.9.5', 'python-daemon>=2.2.4' if not os.name == 'nt' else '', 'Markdown>=3.1.1'],
    extras_require={'keyring': 'keyring>=10.0'}
)
