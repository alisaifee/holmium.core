from holmium.core import Page, Element, Elements, Locators, ElementMap


class GoogleMain(Page):
    search_box = Element( Locators.NAME, "q", timeout = 1)
    google_buttons = ElementMap ( Locators.CLASS_NAME, "gbts" , timeout = 1 )
    search_results = Elements( Locators.CSS_SELECTOR, "li.g", timeout = 1, value = lambda el : {
        "link":el.find_element_by_css_selector("h3.r>a").get_attribute("href"),
        "title":el.find_element_by_css_selector("h3.r>a").text
        })

    def search ( self, query ):
        self.google_buttons["Search"].click() # self.google_buttons behaves just like a dictionary
        self.search_box.clear() # self.search_box is now evaluated directly to a WebElement
        self.search_box.send_keys(query)
        self.search_box.submit()


