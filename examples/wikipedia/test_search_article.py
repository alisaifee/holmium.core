import unittest

import selenium.webdriver

from holmium.core import Page, Element, Locators, ElementMap


class WikiPedia(Page):
    languages = ElementMap(
        Locators.CLASS_NAME, "central-featured-lang"
        , key = lambda el:el.get_attribute("lang")
        , value = lambda el: el.find_element_by_tag_name("a")
    )
    search_box = Element(
        Locators.CSS_SELECTOR, "input#searchInput"
    )
    article_title = Element(
        Locators.CSS_SELECTOR, "h1#firstHeading"
    )
    search_results = ElementMap(
        Locators.CSS_SELECTOR, "div.mw-search-result-heading>a"
    )

    def search(self, query):
        self.search_box.clear()
        self.search_box.send_keys( query )
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
                language
            )

    def tearDown(self):
        self.driver.quit()
