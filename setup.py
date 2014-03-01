#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages
import sys

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
    install_requires=['gmusicapi>=3.1.1-dev', 'netifaces', 'pyxdg', 'eyed3', 'python-daemon'],
    dependency_links = ['https://github.com/simon-weber/Unofficial-Google-Music-API/tarball/develop#egg=gmusicapi-3.1.1-dev']
)
