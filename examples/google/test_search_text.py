import unittest
import selenium.webdriver
from holmium.core import Page, Element, Elements, Locators


class GoogleMain(Page):
    search_box = Element(Locators.NAME, "q", timeout=2)
    search_results = Elements(
        Locators.CSS_SELECTOR,
        "div.rc",
        timeout=2,
        value=lambda el: {
            "link": el.find_element_by_css_selector("div.r>a").get_attribute("href"),
            "title": el.find_element_by_css_selector("div.r>a>h3").text,
        },
    )

    def search(self, query):
        self.search_box.clear()
        self.search_box.send_keys(query)
        self.search_box.submit()


class TextSearchTest(unittest.TestCase):
    def setUp(self):
        self.driver = selenium.webdriver.Firefox()
        self.page = GoogleMain(self.driver, "http://www.google.com")

    def test_text_search(self):
        self.assertTrue(len(self.page.search("selenium testing").search_results) > 0)

    def test_text_search_first_result(self):
        # execute the page object method search
        self.page.search("selenium  testing")
        self.assertEqual(self.page.search_results[0]["title"], "Selenium")
        self.assertEqual(
            self.page.search_results[0]["link"], "https://www.selenium.dev/"
        )

    def tearDown(self):
        self.driver.quit()
