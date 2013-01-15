import unittest
import holmium.core
import selenium.webdriver


class PageElementsTest(unittest.TestCase):
    def setUp(self):
        self.driver = selenium.webdriver.PhantomJS()

    def test_basic_element(self):
        class SimplePage(holmium.core.PageObject):
            el_list_default = holmium.core.PageElements(holmium.core.Locators.CLASS_NAME, "simple_class")
            el_list_valuemapper = holmium.core.PageElements(holmium.core.Locators.CLASS_NAME, "simple_class"
                                                            , value = lambda el: el.find_element_by_tag_name("a").text)
            el_list_valuemapper_complex = holmium.core.PageElements(holmium.core.Locators.CLASS_NAME, "simple_class"
                                                                    , value = lambda el : {
                                                                        "link":el.find_element_by_tag_name("a").get_attribute("href")
                                                                        ,"text" : el.find_element_by_tag_name("a").text } )
            first_el = holmium.core.PageElement( holmium.core.Locators.TAG_NAME, "a" , base_element = el_list_default[0] )

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
        self.assertEquals([k.text for k in page.el_list_default] , ["simple class el 1 element 1", "simple class el 2 element 2", "simple class el 3 element 3"] )
        self.assertEquals(page.el_list_valuemapper , ["element 1", "element 2", "element 3"] )
        self.assertEquals(page.el_list_valuemapper_complex , [{"link":"el1", "text":"element 1"}, {"link":"el2", "text":"element 2"} , {"link":"el3", "text":"element 3"}])
        self.assertEquals(page.first_el.text, "element 1")

