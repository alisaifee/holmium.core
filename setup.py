"""
setup.py for holmium.core


"""
__author__ = "Ali-Akber Saifee"
__email__ = "ali@indydevs.org"
__copyright__ = "Copyright 2014, Ali-Akber Saifee"

from setuptools import setup, find_packages
import os
if __name__ == "__main__":
    this_dir = os.path.abspath(os.path.dirname(__file__))
    REQUIREMENTS = open(
        os.path.join(this_dir, 'requirements/main.txt'), 'rt'
    ).read()

    import versioneer
    long_description = open('README.rst').read() + open('HISTORY.rst').read()
    setup(
        name='holmium.core',
        author=__author__,
        author_email=__email__,
        license="MIT",
        url="https://holmiumcore.readthedocs.org/en/latest/",
        zip_safe=False,
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        install_requires=REQUIREMENTS,
        classifiers=[k for k in open('CLASSIFIERS').read().split('\n') if k],
        description='selenium page objects and other utilities for test creation',  # noqa: E501
        long_description=long_description,
        packages=find_packages(exclude=["tests*"])
    )
