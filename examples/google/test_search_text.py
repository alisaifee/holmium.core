import unittest
import selenium.webdriver
from holmium.core import Page, Element, Elements, Locators, ElementMap


class GoogleMain(Page):
    search_box = Element(Locators.NAME, "q", timeout=2)
    google_buttons = ElementMap(
        Locators.CSS_SELECTOR, ".jsb input", timeout=2,
        key=lambda e: e.get_attribute("value")
    )
    search_results = Elements(
        Locators.CSS_SELECTOR, "div.g>div.rc", timeout=2,
        value = lambda el : {
            "link": el.find_element_by_css_selector("h3.r>a").get_attribute("href"),
            "title": el.find_element_by_css_selector("h3.r>a").text
        }
    )

    def search ( self, query ):
        self.google_buttons["Google Search"].click() # self.google_buttons behaves just like a dictionary
        self.search_box.clear() # self.search_box is now evaluated directly to a WebElement
        self.search_box.send_keys(query)
        self.search_box.submit()


class TextSearchTest(unittest.TestCase):
    def setUp(self):
        self.driver = selenium.webdriver.Firefox()
        self.page = GoogleMain(self.driver, "http://www.google.com")

    def test_text_search(self):
        self.assertTrue(len(self.page.search("selenium").search_results) > 0)

    def test_text_search_first_result(self):
        self.page.search("selenium") # execute the page object method search
        self.assertEquals(
            self.page.search_results[0]["title"],
            u"Selenium - Web Browser Automation"
        )
        self.assertEquals(
            self.page.search_results[0]["link"],
            u"http://www.seleniumhq.org/"
        )

    def tearDown(self):
        self.driver.quit()
