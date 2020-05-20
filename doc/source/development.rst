***********
Development
***********
.. _github: http://github.com/alisaifee/holmium.core/
.. _issue tracker: http://github.com/alisaifee/holmium.core/issues
.. _github actions: https://github.com/alisaifee/holmium.core/actions?query=workflow%3ACI
.. _develop: http://pythonhosted.org/distribute/setuptools.html#development-mode
.. _chromedriver page: https://chromedriver.chromium.org/getting-started

Contributors
============
.. include:: ../../CONTRIBUTORS.rst

Project Resources
=================
Continuous Integration
    The project is being continuously built using `github actions`_ against
    python 2.7, 3.5, 3.7 & 3.8

Code
    The code is hosted on `github`_.

Bugs, Feature Requests
    Tracked at the `issue tracker`_.

Installation
============

.. note::

   Holmium is tested and supported on pythons version 2.7 & 3.5+.

The stable version can be installed either via ``pip`` or ``easy_install``.

.. code-block:: bash

    pip install holmium.core
    # or
    easy_install holmium.core


To use holmium.core directly from source the preferred method is to use the
`develop`_ mode. This will make :mod:`holmium.core` available on your `PATH`,
but will point to the checkout. Any updates made in the checkout will be available
in the *installed* version.

.. code-block:: bash

    git clone git@github.com:alisaifee/holmium.core
    cd holmium.core
    sudo python setup.py develop

Tests
=====
:mod:`holmium.core` uses ``nosetests`` for running its tests. You will also
need ``chromedriver`` installed to run certain tests that make more sense without
mocking. For instructions on installing ``chromedriver`` go to the `chromedriver page`_.

.. code-block:: bash

    cd holmium.core
    nosetests --with-coverage --cover-html --cover-erase --cover-package=holmium.core


