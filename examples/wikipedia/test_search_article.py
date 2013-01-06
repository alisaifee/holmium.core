import pages
import unittest
import selenium.webdriver
from holmium.core import PageElement, Locators
class TextSearchArticle(unittest.TestCase):
    def setUp(self):
        self.driver = selenium.webdriver.Firefox()
        self.page = pages.WikiPedia(self.driver, "http://wikipedia.org")

    def test_text_search_alllangs(self):
        for language in self.page.languages:
            self.page.go_home()
            self.page.languages[language].click()
            self.page.search("google")
            assert self.page.article_title.text == "Google", self.page.article_title.text

    def tearDown(self):
        self.driver.quit()
