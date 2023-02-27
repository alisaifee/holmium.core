.. _PageObjects: http://code.google.com/p/selenium/wiki/PageObjects
.. _Selenium: http://www.seleniumhq.org/
.. |ci| image:: https://github.com/alisaifee/holmium.core/workflows/CI/badge.svg?branch=master
    :target: https://github.com/alisaifee/holmium.core/actions?query=branch%3Amaster+workflow%3ACI
.. |coveralls| image:: https://img.shields.io/coveralls/alisaifee/holmium.core/master.svg?style=flat-square
    :target: https://coveralls.io/r/alisaifee/holmium.core?branch=master
.. |license| image:: https://img.shields.io/pypi/l/holmium.core.svg?style=flat-square
    :target: https://pypi.python.org/pypi/holmium.core
.. |pypi| image:: https://img.shields.io/pypi/v/holmium.core.svg
    :target: https://pypi.python.org/pypi/holmium.core
.. |docs| image:: https://readthedocs.org/projects/holmiumcore/badge
    :target: https://holmiumcore.readthedocs.org


************
holmium.core
************
|ci| |coveralls| |pypi| |docs| |license|


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
            elements = self.driver.find_elements_by_css_selector("div#main_navbar ul li>a")
            self.assertTrue(len(elements) > 0)
            for element in elements:
                self.assertTrue(element.is_displayed())
            expected_link_list = [
              "About",
              "Blog",
              "Documentation",
              "Downloads",
              "English",
              "Projects",
              "Support",
            ]
            actual_link_list = [el.text for el in elements]
            self.assertEqual(sorted(expected_link_list), sorted(actual_link_list))

        def test_projects_selenium_heading(self):
            self.driver.get(self.url)
            projects_link = self.driver.find_element_by_css_selector(
                "nav>a[href='./projects']"
            )
            projects_link.click()
            heading = self.driver.find_element_by_css_selector("p.lead")
            self.assertEqual(heading.text, "Selenium has many projects that combine to form a versatile testing system.")

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

  import unittest

  from holmium.core import Element, ElementMap, Locators, Page, TestCase


  class SeleniumHQPage(Page):
	  nav_links = ElementMap(Locators.CSS_SELECTOR, "div#main_navbar ul li>a")
	  header_text = Element(Locators.CSS_SELECTOR, "p.lead")


  class SeleniumHQTest(TestCase):
	  def setUp(self):
		  self.page = SeleniumHQPage(self.driver, "http://seleniumhq.org")

	  def test_header_links(self):
		  self.assertTrue(len(self.page.nav_links) > 0)
		  self.assertElementsDisplayed(self.page.nav_links)
		  self.assertEqual(
			  sorted(
				  [
					  "About",
					  "Blog",
					  "Documentation",
					  "Downloads",
					  "English",
					  "Projects",
					  "Support",
				  ]
			  ),
			  sorted(self.page.nav_links.keys()),
		  )

	  def test_projects_selenium_heading(self):
		  self.page.nav_links["Projects"].click()
		  self.assertElementTextEqual(
			  self.page.header_text,
			  "Selenium has many projects that combine to form a versatile testing system.",
		  )


  if __name__ == "__main__":
	  unittest.main()


Which can then be executed in a few different ways as shown below.

.. code-block:: bash

    HO_BROWSER=firefox python test_selenium_hq.py


***************
Feature Summary
***************

.. _Unit test integration: http://holmiumcore.readthedocs.org/en/latest/unittest.html
.. _Page Objects: http://holmiumcore.readthedocs.org/en/latest/usage.html
.. _Cucumber Features: http://holmiumcore.readthedocs.org/en/latest/cucumber.html
.. _TestCase: http://holmiumcore.readthedocs.org/en/latest/api.html#holmium.core.TestCase

* Automatic provisioning and configuration of webdriver instances based on
  environment variables
* Shorthand assertions for web pages (`TestCase`_)
* Declarative model for defining pages, sections, page elements and element collections (`Page Objects`_)


