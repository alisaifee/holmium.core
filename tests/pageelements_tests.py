import unittest
import holmium.core
from tests.utils import get_driver, make_temp_page


class ElementsTest(unittest.TestCase):
    def setUp(self):
        self.driver = get_driver()

    def test_basic_element(self):
        class SimplePage(holmium.core.Page):
            el_list_default = holmium.core.Elements(holmium.core.Locators.CLASS_NAME, "simple_class")
            el_list_valuemapper = holmium.core.Elements(holmium.core.Locators.CLASS_NAME, "simple_class"
                                                            , value = lambda el: el.find_element_by_tag_name("a").text)
            el_list_valuemapper_complex = holmium.core.Elements(holmium.core.Locators.CLASS_NAME, "simple_class"
                                                                    , value = lambda el : {
                                                                        "link":el.find_element_by_tag_name("a").get_attribute("href")
                                                                        ,"text" : el.find_element_by_tag_name("a").text } )
            first_el = holmium.core.Element( holmium.core.Locators.TAG_NAME, "a" , base_element = el_list_default[0] )

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
        self.assertEqual([k.text for k in page.el_list_default],
                          ["simple class el 1 element 1",
                           "simple class el 2 element 2",
                           "simple class el 3 element 3"])
        self.assertEqual(page.el_list_valuemapper,
                          ["element 1", "element 2", "element 3"])
        self.assertEqual(page.el_list_valuemapper_complex,
                          [{"link": "http://el1.com/", "text": "element 1"},
                           {"link": "http://el2.com/", "text": "element 2"},
                           {"link": "http://el3.com/", "text": "element 3"}])
        self.assertEqual(page.first_el.text, "element 1")

