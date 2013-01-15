import unittest
from  holmium.core import PageObject, PageElement, Locators
import selenium.webdriver


class PageElementTest(unittest.TestCase):
    page_content = """
            <body>
                <div id="simple_id">simple_id</div>
                <div class="simple_class">simple_class</div>
                <div class="simple_xpath"><h3>Simple XPATH</h3></div>
            </body>
        """

    def setUp(self):
        self.driver = selenium.webdriver.PhantomJS()

    def test_basic_element(self):
        class SimplePage(PageObject):
            id_el = PageElement(Locators.ID, "simple_id")
            class_el = PageElement(Locators.CLASS_NAME, "simple_class")
            selector_el = PageElement(Locators.CSS_SELECTOR, "div.simple_class")
            xpath_el = PageElement(Locators.XPATH, "//div[h3/text()='Simple XPATH']")


        self.driver.execute_script("document.write('%s')" % PageElementTest.page_content.replace('\n',''))
        page = SimplePage(self.driver)
        assert page.id_el.text == "simple_id"
        assert page.class_el.text == "simple_class"
        assert page.selector_el.text == "simple_class"
        assert page.xpath_el.text == "Simple XPATH"


    def test_basic_element_with_dict(self):
        class SimplePage(PageObject):
            elements = { "id": PageElement ( Locators.ID, "simple_id" ), "class" : PageElement(Locators.CLASS_NAME, "simple_class") }


        self.driver.execute_script("document.write('%s')" % PageElementTest.page_content.replace('\n',''))
        page = SimplePage(self.driver)
        assert page.elements["id"].text == "simple_id"
        assert page.elements["class"].text == "simple_class"

    def test_basic_element_with_list(self):
        class SimplePage(PageObject):
            elements = [PageElement ( Locators.ID, "simple_id" ), PageElement(Locators.CLASS_NAME, "simple_class") ]


        self.driver.execute_script("document.write('%s')" % PageElementTest.page_content.replace('\n',''))
        page = SimplePage(self.driver)
        assert page.elements[0].text == "simple_id"
        assert page.elements[1].text == "simple_class"



