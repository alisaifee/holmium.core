"""
setup.py for holmium.core


"""
__author__ = "Ali-Akber Saifee"
__email__ = "ali@indydevs.org"
__copyright__ = "Copyright 2014, Ali-Akber Saifee"

from setuptools import setup, find_packages
import os
import sys
this_dir = os.path.abspath(os.path.dirname(__file__))
REQUIREMENTS = filter(None, open(os.path.join(this_dir, 'requirements.txt')).read().splitlines())

import versioneer
versioneer.versionfile_source = "holmium/core/_version.py"
versioneer.versionfile_build = "holmium/core/version.py"
versioneer.tag_prefix = ""
versioneer.parentdir_prefix = "holmium.core-"

setup(
    name='holmium.core',
    author = __author__,
    author_email = __email__,
    license = open("LICENSE.txt").read(),
    url="https://holmiumcore.readthedocs.org/en/latest/",
    zip_safe = False,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires = REQUIREMENTS,
    classifiers=[k for k in open('CLASSIFIERS').read().split('\n') if k],
    description='selenium page objects and other utilities for test creation',
    long_description=open('README.rst').read() + open('HISTORY.rst').read(),
    packages = find_packages(exclude=["tests*"]),
    entry_points = {
        'nose.plugins.0.10': ['holmium = holmium.core:HolmiumNose',]
        }
)

