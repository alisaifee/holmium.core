import unittest
import holmium.core
import mock
import selenium.webdriver
class DeprecatedPageTest(unittest.TestCase):
    def test_basic_po(self):
        with mock.patch('warnings.warn') as warn:
            class BasicPage(holmium.core.PageObject):
                element = holmium.core.PageElement( holmium.core.Locators.ID, "test_id" )
                elements = holmium.core.PageElements( holmium.core.Locators.ID, "test_id" )
                elementmap = holmium.core.PageElementMap( holmium.core.Locators.ID, "test_id" )
            driver = selenium.webdriver.PhantomJS()
            driver.execute_script('document.write("%s");' % """<body><div id='test_id'>test_text</div></body>""")
            po = BasicPage(driver)
            self.assertEquals( "test_text",  po.element.text)
            self.assertEquals( "test_text",  po.elements[0].text)
            self.assertEquals( "test_id",  po.elementmap["test_text"].get_attribute("id"))
            self.assertTrue( warn.call_count == 4 )
