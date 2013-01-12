import pages
import unittest
import selenium.webdriver
from holmium.core import PageElement, Locators
class TextSearchTest(unittest.TestCase):
    def setUp(self):
        self.driver = selenium.webdriver.Firefox()
        self.page = pages.GoogleMain(self.driver, "http://www.google.com")

    def test_text_search(self):
        self.assertTrue(len(self.page.search("selenium").search_results) > 0)

    def test_text_search_first_result(self):
        self.page.search("selenium") # execute the page object method search
        # extract the a.l element of the first search result
        first_text_result_link = PageElement(Locators.CSS_SELECTOR, "a.l", self.page.search_results[0]).extract()
        assert first_text_result_link.text == "Selenium - Web Browser Automation"

    def tearDown(self):
        self.driver.quit()
