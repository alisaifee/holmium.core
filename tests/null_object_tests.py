import unittest
import time
from StdSuites import anything


from  holmium.core import Page, Element, Locators
from holmium.core.pageobject import NonexistentElement
from tests.utils import get_driver, make_temp_page
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.common.exceptions import TimeoutException, NoSuchFrameException
import hiro



class ElementTest(unittest.TestCase):
    page_content = """
            <body>
                <div id="simple_id">simple_id</div>
                <div id="other_id">simple_id</div>
                <div id="another_id">another_id</div>
                <div class="simple_class">simple_class</div>
                <div class="simple_class">simple_other_class</div>
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

    def test_exception_handling(self):
        class SimplePage(Page):
            id_el = Element(Locators.ID, "simple_id")
            class_el = Element(Locators.CLASS_NAME, "simple_class")
            selector_el = Element(Locators.CSS_SELECTOR, "div.simple_class")
            xpath_el = Element(Locators.XPATH, "//div[h3/text()='Simple XPATH']")
            invalid_el = Element(Locators.ID, "blargh")

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)
       # try:
       #     x=page.invalid_el.text
       # except Exception as e:
       #     assert "NoSuchElementException" in e.message

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


    def test_basic_element_with_only_if(self):

        class SimplePage(Page):
            id_el = Element(Locators.ID, "simple_id")
            id_el_changed = Element(Locators.ID, "simple_id", timeout=10,
                                    only_if=lambda el: el.text == "changed")

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)
        self.assertEqual(page.id_el.text, "simple_id")
        script = 'document.getElementById("simple_id").firstChild.nodeValue="changed";'
        runner = hiro.run_async(5, lambda: time.sleep(1) or self.driver.execute_script(script))
        with hiro.Timeline().scale(10):
            self.assertEqual(page.id_el_changed.text, "changed")
        self.assertTrue(runner.get_response() == None)
        self.driver.refresh()
        with hiro.Timeline().scale(10):
            self.assertEqual(page.id_el_changed, NonexistentElement())

    # test object equivalence/nonequivalence test that expected parameters are displayed

    def test_non_existence_eq_element(self):
        class SimplePage(Page):
            id_el = Element(Locators.ID, "simple_id")
            other_el = Element(Locators.ID, "other_id")
            another_el = Element(Locators.ID, "another_id")

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)
        non_exist_el = NonexistentElement()

        first_el_text =non_exist_el.__eq__(page.id_el.text)
        second_el_text = non_exist_el.__eq__(page.other_el.text)
        third_el_text = non_exist_el.__eq__(page.another_el.text)

        #print first_el_text == second_el_text
        self.assertEqual(first_el_text == third_el_text, second_el_text == third_el_text, "NonExistence __eq__ unit test has failed")

    def test_non_existence_nq_element(self):
        class SimplePage(Page):
            class_el = Element(Locators.CLASS_NAME, "simple_class")
            class_xpath_el = Element(Locators.CLASS_NAME, "simple_xpath")

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)
        non_exist_el = NonexistentElement()

        first_el_text = non_exist_el.__ne__(page.class_el.text)
        second_el_text = non_exist_el.__ne__(page.class_xpath_el.text)

        # print first_el_text == second_el_text
        self.assertEqual(first_el_text != second_el_text, False,
                         "NonExistence __ne__ unit test has failed")

        # test when str() is called on the object test that expected parameters are displayed

    def test_non_existence_str_element(self):
        class SimplePage(Page):
            class_el = Element(Locators.CLASS_NAME, "simple_class")
            exception_msg = "Class Name Found"
            query_string = "key1=value1&key2=value2"

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)
        non_exist_el = NonexistentElement()

        try:
           result = str(NonexistentElement(page.exception_msg,page.class_el.text,page.query_string))
           self.assertIsNotNone(result, "NonExistence __str__ unit test has failed")
        except (WebDriverException) as exception:
            assert exception.__class__.__name__ == page.exception_msg
            raise exception
    # when repr() is called on the object test that expected parameters can be referenced by name. (e.g: object.prop1, object.prop2 etc...)

    def test_non_existence_repr_element(self):
        class SimplePage(Page):
            class_el = Element(Locators.CLASS_NAME, "simple_class")
            exception_msg = "Class Name Found"
            query_string = "key1=value1&key2=value2"

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)
        non_exist_el = NonexistentElement()

        try:
            result = repr(NonexistentElement(page.exception_msg, page.class_el.text, page.query_string))
            self.assertIsNotNone(result,"NonExistence __repr__ unit test has failed")
        except (WebDriverException) as exception:
            assert exception.__class__.__name__ == "simple_class"
            raise exception

    '''test that if an undefined property is referenced, an Exception is thrown that includes the initialization data
            #properties, (exception_class_name, locator_type, query_string)'''
    def test_non_existence_getAttr_element(self):
        class SimplePage(Page):
            class_el = Element(Locators.CLASS_NAME, "simple_class")
            exception_msg = "Class Name Found"
            query_string = "key1=value1&key2=value2"

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)
        non_exist_el = NonexistentElement()

        try:
            result = getattr(NonexistentElement({'webdriver_exception': page.exception_msg, 'locator_type':page.class_el.text, 'query_string':page.query_string}),'locator_type')
            self.assertIsNone(result)
        except (WebDriverException) as exception:
            assert exception.__class__.__name__ == "simple_class"
            raise exception



    if __name__ == "__main__":
        unittest.main()
