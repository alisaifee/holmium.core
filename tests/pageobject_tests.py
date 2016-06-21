import unittest
from holmium.core import Page, Element, Locators, Elements, ElementMap
from holmium.core.pageobject import NonexistentElement
import mock
from tests.utils import get_driver, make_temp_page


class PageTest(unittest.TestCase):
    class BasicPage(Page):
        element = Element( Locators.ID, "test_id" )
    def test_basic_po(self):
        with mock.patch('selenium.webdriver.Firefox') as driver:
            with mock.patch('selenium.webdriver.remote.webelement.WebElement') as element:
                element.tag_name = "div"
                element.text = "test_text"
                driver.find_element.return_value = element
                po = PageTest.BasicPage( driver , iframe = 'some_frame')
                self.assertEqual( "test_text",  po.element.text)

    def test_basic_po_real(self):
        driver = get_driver()
        uri = make_temp_page("""<body><div id='test_id'>test_text</div></body>""")
        po = PageTest.BasicPage(driver, uri)
        self.assertEqual(po.element.text, "test_text")

    def test_all_features(self):
        driver = get_driver()
        content = """
        <div name='e1'>e1</div>
        <div>
            <div name='e2'>e2 - 1
                <div name='e6'>e6</div>
            </div>
            <div name='e2'>e2 - 2</div>
        </div>
        <div>
            <div name='e3'>e3 - 1</div>
            <div name='e3'>e3 - 2</div>
        </div>
        <div name='e4'>e4</div>
        """
        uri = make_temp_page(content)

        driver.get(uri)
        # this may appear weird, but its to test the usecase of providing a WebElement
        # as a base_element. #fml.
        web_element = driver.find_element_by_name("e2")


        class ExhaustivePage(Page):
            element = Element(Locators.NAME, "e1")
            element_invalid = Element(Locators.NAME, "3e")
            elements = Elements(Locators.NAME, "e2")
            elements_invalid = Elements(Locators.NAME, "3e")
            elementmap = ElementMap(Locators.NAME, "e3")
            elementmap_for_ref = ElementMap(Locators.NAME, "e2")
            elementmap_invalid = ElementMap(Locators.NAME, "3e")
            elementmap_raw = { "e4": Element(Locators.NAME, "e4")
                            , "e2": Elements(Locators.NAME, "e2")
                            , "e3": ElementMap(Locators.NAME, "e3")
                            }
            elements_raw = [ Element(Locators.NAME, "e4")
                            , Elements(Locators.NAME, "e2")
                            , ElementMap(Locators.NAME, "e3")
                            ]
            element_list_raw = [
                Element(Locators.NAME, "e4"),
                Element(Locators.NAME, "e6")
            ]
            element_map_raw = {
                "e4":Element(Locators.NAME, "e4"),
                "e6":Element(Locators.NAME, "e6")
            }
            element_second = Element(Locators.NAME, "e2")
            element_ref = Element( Locators.NAME, "e6", base_element = elements[0] )
            element_map_ref = Element( Locators.NAME, "e6", base_element = elementmap_for_ref["e2 - 1\ne6"] )
            element_ref_direct = Element( Locators.NAME, "e6", base_element = element_second )
            element_ref_webelement = Element( Locators.NAME, "e6", base_element = web_element )
            element_ref_invalid = Element( Locators.NAME, "e6", base_element = 42 )

        page = ExhaustivePage(driver)
        self.assertEqual( page.element.text, "e1" )
        self.assertEqual( [el.text for el in page.elements], ["e2 - 1\ne6", "e2 - 2"] )
        self.assertEqual( [(k, k) for k in page.elementmap], [("e3 - 1","e3 - 1"), ("e3 - 2", "e3 - 2")])
        self.assertEqual( [k.text for k in page.element_list_raw], ["e4", "e6"])
        self.assertEqual( sorted([k.text for k in page.element_map_raw.values()]), sorted(["e4", "e6"]))
        v1, v2 = page.element_map_raw.items()
        self.assertEquals(sorted([v1[0], v1[1].text, v2[0], v2[1].text]), sorted(["e4","e4", "e6", "e6"]))
        self.assertEqual( page.elements_raw[0].text, "e4" )
        self.assertEqual( [k.text for k in page.elements_raw[1]], ["e2 - 1\ne6","e2 - 2"])
        self.assertEqual( [k.text for k in page.elements_raw[2].values()], ["e3 - 1","e3 - 2"])
        self.assertEqual( page.elementmap_raw["e4"].text, "e4" )
        self.assertEqual( [k.text for k in page.elementmap_raw["e2"]], ["e2 - 1\ne6", "e2 - 2"])
        self.assertEqual( [k.text for k in page.elementmap_raw["e3"].values()], ["e3 - 1","e3 - 2"])
        self.assertEqual( page.element_ref.text, "e6" )
        self.assertEqual( page.element_ref_direct.text, "e6" )
        self.assertEqual( page.element_ref_webelement.text, "e6" )
        self.assertEqual( page.element_map_ref.text, "e6")
        self.assertRaises( TypeError, lambda: page.element_ref_invalid)
        self.assertEqual( page.element_invalid , NonexistentElement())
        self.assertEqual( page.elements_invalid, [])
        self.assertEqual(page.elementmap_invalid, {})

    def test_fluent(self):
        class FluentPage(Page):
            thing = Element(Locators.NAME, "thing")
            def get_text(self):
                return self.thing.text
            def click_thing(self):
                self.thing.click()
        page = "<div name='thing'>i am thing</div>"
        driver = get_driver()
        uri = make_temp_page(page)
        page = FluentPage(driver, uri)
        self.assertTrue(page.click_thing().get_text(), "i am thing")

