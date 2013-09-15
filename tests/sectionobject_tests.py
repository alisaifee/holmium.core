import unittest
import holmium.core
import mock
import selenium.webdriver
class BasicSection(holmium.core.Section):
    tokens = holmium.core.Elements( holmium.core.Locators.CSS_SELECTOR, "div.token")
class BasicSectionList(holmium.core.Sections):
    tokens = holmium.core.Elements( holmium.core.Locators.CSS_SELECTOR, "div.token")

class BasicPage(holmium.core.Page):
    section = BasicSection(holmium.core.Locators.ID, "section")
    section_2 = BasicSection(holmium.core.Locators.ID, "section_2")
    tokens = holmium.core.Elements( holmium.core.Locators.CLASS_NAME, "token")
class BasicPageWithSections(holmium.core.Page):
    sections = BasicSectionList( holmium.core.Locators.CLASS_NAME, "section")

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
        for i in range(0,2):
            self.assertEquals(po.section.tokens[i].text, "section element %s" % (i+1))
        for i in range(0,2):
            self.assertEquals(po.section_2.tokens[i].text, "section element %s" % (i+3))
        self.assertEquals(po.tokens[0].text, 'section element 1')
        self.assertEquals(po.tokens[1].text, 'section element 2')
        self.assertEquals(po.tokens[2].text, 'section element 3')
        self.assertEquals(po.tokens[3].text, 'section element 4')

    def test_basic_po_with_sections(self):
        driver = selenium.webdriver.PhantomJS()
        page = """
        <body>
            <div class='section'>
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
            <div class='section'>
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
        </body>
        """
        driver.execute_script('document.write("%s");' % page.strip().replace("\n",""))
        po = BasicPageWithSections(driver)
        counter=1
        for section in po.sections:
            for token in section.tokens:
                self.assertEquals(token.text, "section element %s" % counter)
                counter+=1
