"""
setup.py for nosedbreport


"""
__author__ = "Ali-Akber Saifee"
__email__ = "ali@mig33global.com"
__copyright__ = "Copyright 2013, ProjectGoth"

from setuptools import setup, find_packages
import holmium.core
setup(
    name='holmium.core',
    author = __author__,
    author_email = __email__,
    license = "MIT",
    zip_safe = False,
    version=holmium.core.__version__,
    include_package_data = True,
    description='mig33 extensions to python-selenium',
    long_description=open('README.rst').read(),
    packages = ['holmium.core'],
)

