"""
setup.py for holmium.core


"""
__author__ = "Ali-Akber Saifee"
__email__ = "ali@mig33global.com"
__copyright__ = "Copyright 2013, ProjectGoth"

from setuptools import setup
import codecs
import holmium.core
setup(
    name='holmium.core',
    author = __author__,
    author_email = __email__,
    license = "MIT",
    url="https://holmiumcore.readthedocs.org/en/latest/",
    zip_safe = False,
    version=holmium.core.__version__,
    include_package_data = True,
    description='selenium page objects and other utilities for test creation',
    long_description=codecs.open('README.rst').read(),
    packages = ['holmium.core'],
)

