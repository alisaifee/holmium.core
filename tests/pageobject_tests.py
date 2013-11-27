import unittest
import holmium.core
import mock
from tests.utils import get_driver, make_temp_page


class PageTest(unittest.TestCase):
    class BasicPage(holmium.core.Page):
        element = holmium.core.Element( holmium.core.Locators.ID, "test_id" )
    def test_basic_po(self):
        with mock.patch('selenium.webdriver.Firefox') as driver:
            with mock.patch('selenium.webdriver.remote.webelement.WebElement') as element:
                element.tag_name = "div"
                element.text = "test_text"
                driver.find_element.return_value = element
                po = PageTest.BasicPage( driver , iframe = 'some_frame')
                self.assertEquals( "test_text",  po.element.text)

    def test_basic_po_real(self):
        driver = get_driver()
        uri = make_temp_page("""<body><div id='test_id'>test_text</div></body>""")
        po = PageTest.BasicPage(driver, uri)
        self.assertEquals(po.element.text, "test_text")

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


        class ExhaustivePage(holmium.core.Page):
            element = holmium.core.Element(holmium.core.Locators.NAME, "e1")
            element_invalid = holmium.core.Element(holmium.core.Locators.NAME, "3e")
            elements = holmium.core.Elements(holmium.core.Locators.NAME, "e2")
            elements_invalid = holmium.core.Elements(holmium.core.Locators.NAME, "3e")
            elementmap = holmium.core.ElementMap(holmium.core.Locators.NAME, "e3")
            elementmap_for_ref = holmium.core.ElementMap(holmium.core.Locators.NAME, "e2")
            elementmap_invalid = holmium.core.ElementMap(holmium.core.Locators.NAME, "3e")
            elementmap_raw = { "e4": holmium.core.Element(holmium.core.Locators.NAME, "e4")
                            , "e2": holmium.core.Elements(holmium.core.Locators.NAME, "e2")
                            , "e3": holmium.core.ElementMap(holmium.core.Locators.NAME, "e3")
                            }
            elements_raw = [ holmium.core.Element(holmium.core.Locators.NAME, "e4")
                            , holmium.core.Elements(holmium.core.Locators.NAME, "e2")
                            , holmium.core.ElementMap(holmium.core.Locators.NAME, "e3")
                            ]
            element_second = holmium.core.Element(holmium.core.Locators.NAME, "e2")
            element_ref = holmium.core.Element( holmium.core.Locators.NAME, "e6", base_element = elements[0] )
            element_map_ref = holmium.core.Element( holmium.core.Locators.NAME, "e6", base_element = elementmap_for_ref["e2 - 1\ne6"] )
            element_ref_direct = holmium.core.Element( holmium.core.Locators.NAME, "e6", base_element = element_second )
            element_ref_webelement = holmium.core.Element( holmium.core.Locators.NAME, "e6", base_element = web_element )
            element_ref_invalid = holmium.core.Element( holmium.core.Locators.NAME, "e6", base_element = 42 )

        page = ExhaustivePage(driver)
        self.assertEquals( page.element.text, "e1" )
        self.assertEquals( [el.text for el in page.elements], ["e2 - 1\ne6", "e2 - 2"] )
        self.assertEquals( [(k, k) for k in page.elementmap], [("e3 - 1","e3 - 1"), ("e3 - 2", "e3 - 2")])
        self.assertEquals( page.elements_raw[0].text, "e4" )
        self.assertEquals( [k.text for k in page.elements_raw[1]], ["e2 - 1\ne6","e2 - 2"])
        self.assertEquals( [k.text for k in page.elements_raw[2].values()], ["e3 - 1","e3 - 2"])
        self.assertEquals( page.elementmap_raw["e4"].text, "e4" )
        self.assertEquals( [k.text for k in page.elementmap_raw["e2"]], ["e2 - 1\ne6", "e2 - 2"])
        self.assertEquals( [k.text for k in page.elementmap_raw["e3"].values()], ["e3 - 1","e3 - 2"])
        self.assertEquals( page.element_ref.text, "e6" )
        self.assertEquals( page.element_ref_direct.text, "e6" )
        self.assertEquals( page.element_ref_webelement.text, "e6" )
        self.assertEquals( page.element_map_ref.text, "e6")
        self.assertRaises( TypeError, lambda: page.element_ref_invalid)
        self.assertEquals( page.element_invalid , None)
        self.assertEquals( page.elements_invalid, [])
        self.assertEquals(page.elementmap_invalid, {})

    def test_fluent(self):
        class FluentPage(holmium.core.Page):
            thing = holmium.core.Element(holmium.core.Locators.NAME, "thing")
            def get_text(self):
                return self.thing.text
            def click_thing(self):
                self.thing.click()
        page = "<div name='thing'>i am thing</div>"
        driver = get_driver()
        uri = make_temp_page(page)
        page = FluentPage(driver, uri)
        self.assertTrue(page.click_thing().get_text(), "i am thing")

