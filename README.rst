.. _PageObjects: http://code.google.com/p/selenium/wiki/PageObjects

Introduction
============
holmium.core provides utility classes to simplify writing pageobjects for webpages using selenium.

Nothing beats an example. Conventionally unit tests integrating with python-selenium are written similarly to the following code block.

::

    # -*- coding: utf-8 -*-
    import selenium.webdriver
    import unittest



    class PythonOrgTest(unittest.TestCase):
        def setUp(self):
            self.driver = selenium.webdriver.Firefox()

        def test_links(self):
            self.driver.get("http://www.python.org")
            elements = self.driver.find_elements_by_css_selector("ul.level-one li>a")
            assert len(elements) > 0
            link_list = [u"ABOUT", u"NEWS", u"DOCUMENTATION"
                        , u"DOWNLOAD", u"下载", u"COMMUNITY"
                        , u"FOUNDATION", u"CORE DEVELOPMENT"]
            for element in zip(elements, link_list):
                assert element[0].text == element[1], element[0].text

        def test_about_python_heading(self):
            self.driver.get("http://www.python.org")
            elements = self.driver.find_elements_by_css_selector("ul.level-one li>a")
            about_link = [ k for k in elements if k.text == u"ABOUT"][0]
            about_link.click()
            h1_title = self.driver.find_element_by_css_selector("h1.title")
            assert h1_title.text == u"About Python"

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


::
  
    # -*- coding: utf-8 -*-
    from holmium.core import HolmiumTestCase, PageObject, PageElement, PageElementMap, PageElements, Locators

    class PythonOrgPage(PageObject):
        side_bar_links = PageElementMap( Locators.CSS_SELECTOR
                                            , "ul.level-one li"
                                            , key = lambda element : element.find_element_by_tag_name("a").text
                                            , value = lambda element: element.find_element_by_tag_name("a") )
        header_text = PageElement(Locators.CSS_SELECTOR, "h1.title")

    class PythonOrgTest(HolmiumTestCase):
        def setUp(self):
            self.page = PythonOrgPage(self.driver, "http://www.python.org")

        def test_links(self):
            self.page.go_home()
            assert len(self.page.side_bar_links) > 0
            link_list = [u"ABOUT", u"NEWS", u"DOCUMENTATION"
                        , u"DOWNLOAD", u"下载", u"COMMUNITY"
                        , u"FOUNDATION", u"CORE DEVELOPMENT"]
            assert self.page.side_bar_links.keys() == link_list

        def test_about_python_heading(self):
            self.page.go_home()
            self.page.side_bar_links[u"ABOUT"].click()
            assert self.page.header_text.text == u"About Python"


