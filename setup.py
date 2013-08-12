"""
setup.py for holmium.core


"""
__author__ = "Ali-Akber Saifee"
__email__ = "ali@mig33global.com"
__copyright__ = "Copyright 2013, ProjectGoth"

from setuptools import setup, find_packages
import os
import sys
import holmium.version
this_dir = os.path.abspath(os.path.dirname(__file__))
REQUIREMENTS = filter(None, open(os.path.join(this_dir, 'requirements.txt')).read().splitlines())
extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True


setup(
    name='holmium.core',
    author = __author__,
    author_email = __email__,
    license = "MIT",
    url="https://holmiumcore.readthedocs.org/en/latest/",
    zip_safe = False,
    version=holmium.version.__version__,
    include_package_data = True,
    install_requires = REQUIREMENTS,
    description='selenium page objects and other utilities for test creation',
    long_description=open('README.rst').read() + open('HISTORY.rst').read(),
    packages = find_packages(),
    entry_points = {
        'nose.plugins.0.10': ['holmium = holmium.core:HolmiumNose',]
        },
    **extra
)

