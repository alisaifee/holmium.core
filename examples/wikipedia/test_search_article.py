import pages
import unittest
import selenium.webdriver

class TextSearchArticle(unittest.TestCase):
    def setUp(self):
        self.driver = selenium.webdriver.Firefox()
        self.page = pages.WikiPedia(self.driver, "http://wikipedia.org")

    def test_text_search_alllangs(self):
        for language in self.page.languages:
            self.page.go_home().languages[language].click()
            self.assertEquals(self.page.search("google").article_title.text, "Google", language)

    def tearDown(self):
        self.driver.quit()
