import unittest
import holmium.core
import mock
import selenium.webdriver
class BasicSection(holmium.core.Section):
    tokens = holmium.core.Elements( holmium.core.Locators.CSS_SELECTOR, "div.token")
class BasicPage(holmium.core.Page):
    section = BasicSection(holmium.core.Locators.ID, "section")
    section_2 = BasicSection(holmium.core.Locators.ID, "section_2")
    tokens = holmium.core.Elements( holmium.core.Locators.CLASS_NAME, "token")
class SectionTest(unittest.TestCase):
    def test_basic_po_real(self):
        driver = selenium.webdriver.PhantomJS()
        page = """
        <body>
            <div id='section'>
                <div class='token'>
                    <div class='el'>
                        section element 1
                    </div>
                </div>
                <div class='token'>
                    <div class='el'>
                        section element 2
                    </div>
                </div>
            </div>
            <div id='section_2'>
                <div class='token'>
                    <div class='el'>
                        section element 3
                    </div>
                </div>
                <div class='token'>
                    <div class='el'>
                        section element 4
                    </div>
                </div>
            </div>
            <span class='token'>
                <div class='el'>
                    element 5
                </div>
            </span>
        </body>
        """
        driver.execute_script('document.write("%s");' % page.strip().replace("\n",""))
        po = BasicPage(driver)
        self.assertEquals(len(po.tokens), 5)
        self.assertEquals(len(po.section.tokens), 2)
        self.assertEquals(len(po.section_2.tokens), 2)
