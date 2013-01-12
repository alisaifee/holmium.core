from holmium.core import PageObject, PageElement, PageElements, Locators, PageElementMap


class GoogleMain(PageObject):
    search_box = PageElement( Locators.NAME, "q", timeout = 1)
    google_buttons = PageElementMap ( Locators.CLASS_NAME, "gbts" , timeout = 1 )
    search_results = PageElements( Locators.CSS_SELECTOR, "li.g", timeout = 1)

    def search ( self, query ):
        self.google_buttons["Search"].click() # self.google_buttons behaves just like a dictionary
        self.search_box.clear() # self.search_box is now evaluated directly to a WebElement
        self.search_box.send_keys(query)
        self.search_box.submit()


