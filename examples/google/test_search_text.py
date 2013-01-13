import pages
import unittest
import selenium.webdriver
class TextSearchTest(unittest.TestCase):
    def setUp(self):
        self.driver = selenium.webdriver.Firefox()
        self.page = pages.GoogleMain(self.driver, "http://www.google.com")

    def test_text_search(self):
        self.assertTrue(len(self.page.search("selenium").search_results) > 0)

    def test_text_search_first_result(self):
        self.page.search("selenium") # execute the page object method search
        self.assertEquals( self.page.search_results[0]["title"], "Selenium - Web Browser Automation")
        self.assertEquals( self.page.search_results[0]["link"], "http://seleniumhq.org/")

    def tearDown(self):
        self.driver.quit()
