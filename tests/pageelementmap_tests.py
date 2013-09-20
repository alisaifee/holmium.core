import unittest
import holmium.core
import selenium.webdriver


class ElementMapTest(unittest.TestCase):
    def setUp(self):
        self.driver = selenium.webdriver.PhantomJS()

    def test_basic_element(self):
        class SimplePage(holmium.core.Page):
            el_map_default = holmium.core.ElementMap(holmium.core.Locators.CLASS_NAME, "simple_class")
            el_map_keymapper = holmium.core.ElementMap(holmium.core.Locators.CLASS_NAME, "simple_class"
                                                            , key = lambda el: el.find_element_by_tag_name("a").text)
            el_map_valuemapper = holmium.core.ElementMap(holmium.core.Locators.CLASS_NAME, "simple_class"
                                                            , value = lambda el: el.find_element_by_tag_name("a").text)
            el_map_keyvaluemapper = holmium.core.ElementMap(holmium.core.Locators.CLASS_NAME, "simple_class"
                                                            , key = lambda el: el.find_element_by_tag_name("a").text
                                                            , value = lambda el: el.find_element_by_tag_name("a").get_attribute("href"))


        self.driver.execute_script("document.write('%s')" % """
            <body>
                <div class="simple_class">
                    simple class el 1
                    <a href="el1">element 1</a>
                </div>
                <div class="simple_class">
                    simple class el 2
                    <a href="el2">element 2</a>
                </div>
                <div class="simple_class">
                    simple class el 3
                    <a href="el3">element 3</a>
                </div>
            </body>
        """.replace('\n',''))
        page = SimplePage(self.driver)
        self.assertEquals(page.el_map_default.keys() , ["simple class el 1 element 1", "simple class el 2 element 2", "simple class el 3 element 3"] )
        self.assertEquals(page.el_map_keymapper.keys() , ["element 1", "element 2", "element 3"] )
        self.assertEquals(page.el_map_valuemapper.values() , ["element 1", "element 2", "element 3"] )
        self.assertEquals(page.el_map_keyvaluemapper.keys() , ["element 1", "element 2", "element 3"] )
        self.assertEquals(page.el_map_keyvaluemapper.values() , ["el1", "el2", "el3"] )

    def tearDown(self):
        if self.driver:
            self.driver.quit()
