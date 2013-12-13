import unittest
import hiro
from holmium.core import ElementMap, Locators, Page
from tests.utils import get_driver, make_temp_page


class ElementMapTest(unittest.TestCase):
    def setUp(self):
        self.driver = get_driver()

    def test_basic_element(self):
        class SimplePage(Page):
            el_map_default = ElementMap(Locators.CLASS_NAME, "simple_class")
            el_map_keymapper = ElementMap(Locators.CLASS_NAME, "simple_class"
                                                            , key = lambda el: el.find_element_by_tag_name("a").text)
            el_map_valuemapper = ElementMap(Locators.CLASS_NAME, "simple_class"
                                                            , value = lambda el: el.find_element_by_tag_name("a").text)
            el_map_keyvaluemapper = ElementMap(Locators.CLASS_NAME, "simple_class"
                                                            , key = lambda el: el.find_element_by_tag_name("a").text
                                                            , value = lambda el: el.find_element_by_tag_name("a").get_attribute("href"))


        uri = make_temp_page("""
            <body>
                <div class="simple_class">
                    simple class el 1
                    <a href="http://el1.com/">element 1</a>
                </div>
                <div class="simple_class">
                    simple class el 2
                    <a href="http://el2.com/">element 2</a>
                </div>
                <div class="simple_class">
                    simple class el 3
                    <a href="http://el3.com/">element 3</a>
                </div>
            </body>
        """)
        page = SimplePage(self.driver, uri)
        self.assertEqual(list(page.el_map_default.keys()) , ["simple class el 1 element 1", "simple class el 2 element 2", "simple class el 3 element 3"] )
        self.assertEqual(list(page.el_map_keymapper.keys()) , ["element 1", "element 2", "element 3"] )
        self.assertEqual(list(page.el_map_valuemapper.values()) , ["element 1", "element 2", "element 3"] )
        self.assertEqual(list(page.el_map_keyvaluemapper.keys()) , ["element 1", "element 2", "element 3"] )
        self.assertEqual(list(page.el_map_keyvaluemapper.values()) , ["http://el1.com/", u"http://el2.com/", u"http://el3.com/"])

    def test_missing_elements(self):
        class SimplePage(Page):
            el_list = ElementMap(Locators.CLASS_NAME,
                                            "element")
            el_list_wait = ElementMap(
                Locators.CLASS_NAME, "elements", timeout=1)
            el_list_only_if = ElementMap(
                Locators.CLASS_NAME, "elements", timeout=1,
                only_if=lambda els: len(els) == 1)

        uri = make_temp_page("""
            <body>
                <div class="_">
                </div>
            </body>
        """)
        with hiro.Timeline().scale(10):
            page = SimplePage(self.driver, uri)
            self.assertEqual(page.el_list, {})
            self.assertEqual(page.el_list_wait, {})
            self.assertEqual(page.el_list_only_if, {})
            uri = make_temp_page("""
                <body>
                    <div class="elements">
                        element_text
                    </div>
                </body>
            """)
            page = SimplePage(self.driver, uri)
            self.assertEqual(page.el_list, {})
            self.assertEqual(len(page.el_list_wait), 1)
            self.assertEqual(len(page.el_list_only_if), 1)