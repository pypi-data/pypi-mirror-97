#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='fstotv',
    version='1.0.3',
    description='send video in local to chromecast',
    author='Alberto Galera Jimenez',
    author_email='galerajimenez@gmail.com',
    url='https://github.com/agalera/fstotv',
    packages=find_packages(),
    # py_modules=['fstotv'],
    install_requires=['pychromecast', 'bottle'],
    entry_points={
        'console_scripts': ['fstotv = fstotv:start']
        },
    )
