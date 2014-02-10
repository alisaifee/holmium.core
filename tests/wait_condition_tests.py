import unittest
import hiro
import time
from tests.utils import make_temp_page, get_driver
from holmium.core import Page, Element, Locators
from holmium.core.conditions import *

class WaitConditionTests(unittest.TestCase):
    def setUp(self):
        self.driver = get_driver()
        self.uri = make_temp_page("<div id='simple_id'>default text</div>")

    def run_script(self, script, delay=0, sync=False):
        return (hiro.run_sync if sync else hiro.run_async)(1, lambda: time.sleep(delay) or self.driver.execute_script(script))

    def build_page_object(self, condition):
        class P(Page):
            id_el = Element(Locators.ID, "simple_id"
                , only_if=condition
                , timeout=5)
        return P

    @hiro.Timeline(scale=10)
    def test_only_if_matches_text(self):
        page = self.build_page_object(MATCHES_TEXT("changed"))(self.driver, self.uri)
        self.assertTrue(page.id_el is None)
        runner = self.run_script('document.getElementById("simple_id").innerHTML="changed";', 1)
        self.assertEqual(page.id_el.text, "changed")


    @hiro.Timeline(scale=10)
    def test_only_if_displayed(self):
        page = self.build_page_object(VISIBLE())(self.driver, self.uri)
        runner = self.run_script('document.getElementById("simple_id").style.display="none";', sync=True)
        runner = self.run_script('document.getElementById("simple_id").style.display="block";', 1)
        self.assertTrue(page.id_el is not None)

    @hiro.Timeline(scale=10)
    def test_only_if_invisible(self):
        page = self.build_page_object(INVISIBLE())(self.driver, self.uri)
        self.assertTrue(page.id_el is None)
        runner = self.run_script('document.getElementById("simple_id").style.display="none";', 1)
        self.assertTrue(page.id_el is not None)

