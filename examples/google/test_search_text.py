import unittest
import selenium.webdriver
from holmium.core import Page, Element, Elements, Locators, ElementMap

class GoogleMain(Page):
    search_box = Element( Locators.NAME, "q", timeout = 1)
    google_buttons = ElementMap ( Locators.CLASS_NAME, "gbts" , timeout = 1 )
    search_results = Elements( Locators.CSS_SELECTOR, "li.g>div.rc", timeout = 1, value = lambda el : {
        "link":el.find_element_by_css_selector("h3.r>a").get_attribute("href"),
        "title":el.find_element_by_css_selector("h3.r>a").text
        })

    def search ( self, query ):
        self.google_buttons["Search"].click() # self.google_buttons behaves just like a dictionary
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
        self.assertEquals( self.page.search_results[0]["title"], "Selenium - Web Browser Automation")
        self.assertEquals( self.page.search_results[0]["link"], "http://docs.seleniumhq.org/")

    def tearDown(self):
        self.driver.quit()
