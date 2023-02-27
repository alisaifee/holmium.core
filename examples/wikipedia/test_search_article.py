import unittest

import selenium.webdriver
from holmium.core import Element, ElementMap, Locators, Page
from holmium.core.conditions import VISIBLE
from selenium.webdriver.common.by import By


class WikiPedia(Page):
    languages = ElementMap(
        Locators.CLASS_NAME,
        "central-featured-lang",
        key=lambda el: el.get_attribute("lang"),
        value=lambda el: el.find_element(By.TAG_NAME, "a"),
    )
    search_box = Element(Locators.CSS_SELECTOR, "input#searchInput")
    article_title = Element(
        Locators.CSS_SELECTOR, "h1#firstHeading", only_if=VISIBLE(), timeout=5
    )
    search_results = ElementMap(Locators.CSS_SELECTOR, "div.mw-search-result-heading>a")

    def search(self, query):
        self.search_box.clear()
        self.search_box.send_keys(query)
        self.search_box.submit()


class TextSearchArticle(unittest.TestCase):
    def setUp(self):
        self.driver = selenium.webdriver.Firefox()
        self.page = WikiPedia(self.driver, "http://wikipedia.org")

    def test_text_search_alllangs(self):
        for language in self.page.languages:
            self.page.go_home().languages[language].click()
            self.assertTrue(
                self.page.search("google").article_title.text.startswith("Google"),
                language,
            )

    def tearDown(self):
        self.driver.quit()
