import unittest
from  holmium.core import Page, Element, Locators
from tests.utils import get_driver, make_temp_page


class ElementTest(unittest.TestCase):
    page_content = """
            <body>
                <div id="simple_id">simple_id</div>
                <div class="simple_class">simple_class</div>
                <div class="simple_xpath"><h3>Simple XPATH</h3></div>
            </body>
        """

    def setUp(self):
        self.driver = get_driver()

    def test_basic_element(self):
        class SimplePage(Page):
            id_el = Element(Locators.ID, "simple_id")
            class_el = Element(Locators.CLASS_NAME, "simple_class")
            selector_el = Element(Locators.CSS_SELECTOR, "div.simple_class")
            xpath_el = Element(Locators.XPATH, "//div[h3/text()='Simple XPATH']")


        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)
        assert page.id_el.text == "simple_id"
        assert page.class_el.text == "simple_class"
        assert page.selector_el.text == "simple_class"
        assert page.xpath_el.text == "Simple XPATH"


    def test_basic_element_with_dict(self):
        class SimplePage(Page):
            elements = { "id": Element ( Locators.ID, "simple_id" ), "class" : Element(Locators.CLASS_NAME, "simple_class") }


        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)
        assert page.elements["id"].text == "simple_id"
        assert page.elements["class"].text == "simple_class"

    def test_basic_element_with_list(self):
        class SimplePage(Page):
            elements = [Element ( Locators.ID, "simple_id" ), Element(Locators.CLASS_NAME, "simple_class") ]

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)
        assert page.elements[0].text == "simple_id"
        assert page.elements[1].text == "simple_class"


