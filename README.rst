.. _PageObjects: http://code.google.com/p/selenium/wiki/PageObjects

Introduction
============
holmium.core provides utility classes to simplify writing pageobjects for webpages using selenium.

Nothing beats an example. Conventionally unit tests integrating with python-selenium are written similarly to the following code block (using seleniumhq.org).

.. code:: python

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


The above example does what most selenium tests do:

* initialize a webdriver upon setUp
* query for one or more web elements using either class name, id, css_selector or xpath 
* assert on the number of occurances / value of certain elements.
* tear down the webdriver after each test case 

It suffers from the typical web development problem of coupling the test case with the HTML plumbing of the page its testing rather than the functionality its meant to excercise.
The concept of `PageObjects`_ reduces this coupling and allow for test authors to separate the layout of the page under test and the functional behavior being tested. This separation also results 
in more maintainable test code (i.e. if an element name changes - all tests dont have to be updated, just the pageobject).

Lets take the above test case for a spin with holmium. Take note of the following:

* The initialization and reset of the webdriver is delegated to the HolmiumTestCase base class
* the page elements are accessed in the test only via PageElement & PageElementMap.


.. code:: python
  
    from holmium.core import HolmiumTestCase, PageObject, PageElement, Locators, PageElementMap


    class SeleniumHQPage(PageObject):
        nav_links = PageElementMap( Locators.CSS_SELECTOR
                                            , "div#header ul>li"
                                            , key = lambda element : element.find_element_by_tag_name("a").text
                                            , value = lambda element: element.find_element_by_tag_name("a") )

        header_text = PageElement(Locators.CSS_SELECTOR, "#mainContent>h2")


    class SeleniumHQTest(HolmiumTestCase):
        def setUp(self):
            self.page = SeleniumHQPage(self.driver, "http://seleniumhq.org")

        def test_header_links(self):
            self.assertTrue( len(self.page.nav_links) > 0 )
            self.assertEquals( sorted(["Projects", "Download", "Documentation", "Support", "About"])
                            ,  sorted(self.page.nav_links.keys() ) )

        def test_about_selenium_heading(self):
            self.page.nav_links["About"].click()
            self.assertEquals(self.page.header_text.text, "About Selenium")



