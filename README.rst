.. _PageObjects: http://code.google.com/p/selenium/wiki/PageObjects
.. _Selenium: http://www.seleniumhq.org/
.. |travis-ci| image:: https://secure.travis-ci.org/alisaifee/holmium.core.png?branch=master
    :target: https://travis-ci.org/#!/alisaifee/holmium.core?branch=master
.. |coveralls| image:: https://coveralls.io/repos/alisaifee/holmium.core/badge.png?branch=master
    :target: https://coveralls.io/r/alisaifee/holmium.core?branch=master

.. |pypi| image:: https://pypip.in/v/holmium.core/badge.png
    :target: https://crate.io/packages/holmium.core/

************
holmium.core
************
|travis-ci| |coveralls| |pypi|


************
Introduction
************

holmium.core provides utilities for simplifying the creation and maintenance of tests that rely on `Selenium`_.

Nothing beats an example. Conventionally automated tests integrating with python-selenium are written
similarly to the following code block (using seleniumhq.org).

.. code-block:: python

    import selenium.webdriver
    import unittest

    class SeleniumHQTest(unittest.TestCase):
        def setUp(self):
            self.driver = selenium.webdriver.Firefox()
            self.url = "http://seleniumhq.org"
        def test_header_links(self):
            self.driver.get(self.url)
            elements = self.driver.find_elements_by_css_selector("div#header ul>li")
            self.assertTrue(len(elements) > 0)
            expected_link_list = ["Projects", "Download", "Documentation", "Support", "About"]
            actual_link_list = [el.text for el in elements]
            self.assertEquals( sorted(expected_link_list), sorted(actual_link_list))

        def test_about_selenium_heading(self):
            self.driver.get(self.url)
            about_link = self.driver.find_element_by_css_selector("div#header ul>li#menu_about>a")
            about_link.click()
            heading = self.driver.find_element_by_css_selector("#mainContent>h2")
            self.assertEquals(heading.text, "About Selenium")

        def tearDown(self):
            if self.driver:
                self.driver.quit()

    if __name__ == "__main__":
        unittest.main()



The above example does what most selenium tests do:

* initialize a webdriver upon setUp
* query for one or more web elements using either class name, id, css_selector or xpath
* assert on the number of occurrences / value of certain elements.
* tear down the webdriver after each test case

It suffers from the typical web development problem of coupling the test case with the HTML plumbing of
the page its testing rather than the functionality its meant to exercise. The concept of `PageObjects`_
reduces this coupling and allow for test authors to separate the layout of the page under test and the
functional behavior being tested. This separation also results in more maintainable test code
(*i.e. if an element name changes - all tests don't have to be updated, just the PageObject*).

Lets take the above test case for a spin with holmium. Take note of the following:

* The initialization and reset of the webdriver is delegated to the TestCase base class
  (*alternatively the class could subclass unittest.TestCase and be run with the holmium nose plugin*).
* the page elements are accessed in the test only via Element & ElementMap.


.. code-block:: python

    from holmium.core import TestCase, Page, Element, Locators, ElementMap
    import unittest

    class SeleniumHQPage(Page):
        nav_links = ElementMap( Locators.CSS_SELECTOR
                                , "div#header ul>li"
                                , key = lambda element : element.find_element_by_tag_name("a").text
                                , value = lambda element: element.find_element_by_tag_name("a") )

        header_text = Element(Locators.CSS_SELECTOR, "#mainContent>h2")


    class SeleniumHQTest(TestCase):
        def setUp(self):
            self.page = SeleniumHQPage(self.driver, "http://seleniumhq.org")

        def test_header_links(self):
            self.assertTrue( len(self.page.nav_links) > 0 )
            self.assertEquals( sorted(["Projects", "Download", "Documentation", "Support", "About"])
                            ,  sorted(self.page.nav_links.keys() ) )

        def test_about_selenium_heading(self):
            self.page.nav_links["About"].click()
            self.assertEquals(self.page.header_text.text, "About Selenium")

    if __name__ == "__main__":
        unittest.main()

Which can then be executed in a few different ways as shown below.

.. code-block:: bash

    # if using TestCase as the base class run as:
    HO_BROWSER=firefox nosetests test_selenium_hq.py
    # or..
    HO_BROWSER=firefox python test_selenium_hq.py
    # if using unittest.TestCase as the base class run as:
    nosetests test_selenium_hq.py --with-holmium --holmium-browser=firefox


***************
Feature Summary
***************

.. _Unit test integration: http://holmiumcore.readthedocs.org/en/latest/unittest.html
.. _Page Objects: http://holmiumcore.readthedocs.org/en/latest/usage.html
.. _Cucumber Features: http://holmiumcore.readthedocs.org/en/latest/cucumber.html
.. _TestCase: http://holmiumcore.readthedocs.org/en/latest/api.html#holmium.core.TestCase

* Automatic provisioning and configuration of webdriver instances based either on environment variables or nosetest arguments. (`Unit test integration`_)
* Shorthand assertions for web pages (`TestCase`_)
* Declarative model for defining pages, sections, page elements and element collections (`Page Objects`_)
* Built in cucumber step definitions for accessing and navigating pages (`Cucumber Features`_)


