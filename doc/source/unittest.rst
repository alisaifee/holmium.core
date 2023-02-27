*********************
Unit Test Integration
*********************
.. currentmodule:: holmium.core

Holmium provides two utilities to ease integration with automated tests.


.. _testing-unittest:

The TestCase base class
================================
This base class extends :class:`unittest.TestCase` and adds the following functionality:

    * automatically provision any number of selenium webdrivers (:attr:`driver`/:attr:`drivers`) to the testcase
      based on the environment variable HO_BROWSER. The webdrivers are generated lazily upon access of the :attr:`driver` or :attr:`drivers`
      attributes.
    * A remote selenium server can also be used by setting the value of HO_REMOTE to the fully qualified url to the selenium server (e.g. http://localhost:4444/wd/hub)
    * clears the browser cookies between each test case
    * quits the driver(s) at the end of the test class or at the end of the test run (depending on the configuration).
    * extra assertion methods relevant to :class:`selenium.webdriver.remote.webelement.WebElement` (refer to :class:`TestCase`)

The following environment variables are respected by :class:`TestCase` when :meth:`unittest.TestCase.setUpClass` is executed.

.. _testing-environment-variables:

Environment Variables
---------------------
===========================  ===========================================================================================================================================
variable                     description
===========================  ===========================================================================================================================================
``HO_BROWSER``               one of chrome,firefox,opera,safari, ie,phantomjs,android,iphone or ipad
``HO_REMOTE``                the full qualified url of the selenium server. If not provided the browsers will be attempted to be launched using the built in webdrivers.
``HO_USERAGENT``             useragent to use as an override. only works with firefox & chrome
``HO_IGNORE_SSL_ERRORS``     ignore ssl errors when accessing pages served under untrusted certificates (default False).
``HO_BROWSER_PER_TEST``      if the variable is set the browser is created/destroyed for each test class (default False).
===========================  ===========================================================================================================================================



Example test case
-----------------

.. code-block:: python

    import unittest
    import holmium.core

    class SimpleTest(holmium.core.TestCase):
        def setUp(self):
            self.driver.get("http://www.google.com")

        def test_title(self):
            self.assertEqual(self.driver.title, "Google")

    if __name__ == "__main__":
        unittest.main()

Execution
---------

.. code-block:: bash

    # against the builtin firefox driver
    HO_BROWSER=firefox python test_simple.py
    # against a firefox instance under a remote selenium server
    HO_BROWSER=firefox HO_REMOTE=http://localhost:5555/wd/hub python test_simple.py

