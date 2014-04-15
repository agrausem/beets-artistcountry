#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='beets-artistcountry',
    version='0.1.1',
    namespace_packages=['beetsplug'],
    packages=['beetsplug'],
    author='Arnaud Grausem',
    author_email='arnaud.grausem@gmail.com',
    description='Beets plugin to retrieve the country of an artist from musicbrainz',
    long_description=open('README.rst').read(),
    url='https://github.com/agrausem/beets-artistcountry',
    install_requires=[
        'beets',
        'musicbrainzngs'
    ]
)
