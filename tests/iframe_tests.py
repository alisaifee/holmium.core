import mock
import unittest
from  holmium.core import Page, Element, Elements, Section, Locators
from tests.utils import get_driver, make_temp_page


class BasicSectionIframe(Section):
    element = Element( Locators.CLASS_NAME, "frame_el")
class BasicPageIframe(Page):
    element = Element( Locators.CLASS_NAME, "frame_el" )
    elements = Elements( Locators.CLASS_NAME, "frame_el" )
    frame_1 = BasicSectionIframe(Locators.CLASS_NAME, "section", "frame_1")
    frame_2 = BasicSectionIframe(Locators.CLASS_NAME, "section", "frame_2")
class BasicPage(Page):
    element = Element( Locators.ID, "test_id" )

class IFrameTest(unittest.TestCase):
    def setUp(self):
        self.driver = get_driver()
    def test_basic_po_with_frame(self):
        frame1 = "<html><body><div class='section'><div class='frame_el'>frame 1 el</div></div></body></html>"
        frame2 = "<html><body><div class='section'><div class='frame_el'>frame 2 el</div></div></body></html>"

        open("/var/tmp/frame1.html","w").write(frame1)
        open("/var/tmp/frame2.html","w").write(frame2)

        p1 = '<html><body><iframe id="frame_1" src="file:///var/tmp/frame1.html"/></body></html>'
        p2 = '<html><body><iframe id="frame_1" src="file:///var/tmp/frame1.html"></iframe><iframe id="frame_2" src="file:///var/tmp/frame2.html"></iframe></body></html>'

        driver = get_driver()
        uri = make_temp_page(p1)
        with mock.patch("holmium.core.log") as log:
            p = BasicPageIframe(driver, uri, iframe="frame_1")
            self.assertEquals(p.element.text, "frame 1 el")
            self.assertEquals(p.frame_1.element.text, "frame 1 el")
            self.assertTrue(p.frame_2.element == None)
            uri = make_temp_page(p2)
            driver.get(uri)
            self.assertTrue(p.frame_2.element != None)
            self.assertEquals(p.frame_2.element.text, "frame 2 el")
            self.assertEquals(p.elements[0].text, "frame 1 el")
            self.assertEquals(log.error.call_count, 1)

    def test_mocked_basic_po_with_frame(self):
        with mock.patch('selenium.webdriver.Firefox') as driver:
            with mock.patch('selenium.webdriver.remote.webelement.WebElement') as element:
                element.tag_name = "div"
                element.text = "test_text"
                driver.find_element.return_value = element
                po = BasicPage( driver , iframe='frame')
                self.assertEquals( "test_text",  po.element.text)
                driver.switch_to_frame.assert_called_with("frame")
                self.assertEquals(driver.switch_to_frame.call_count, 1)
                self.assertEquals(driver.switch_to_default_content.call_count, 1)

