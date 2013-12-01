# -*- coding: utf-8 -*-
import unittest
import threading
import os

import mock

import holmium.core


support = os.path.join(os.path.dirname(__file__), "support")


class BugReports(unittest.TestCase):
    def test_multiple_pageinstances(self):
        """ https://github.com/alisaifee/holmium.core/issues/4
        """
        class p(holmium.core.Page):
            el = holmium.core.Element(holmium.core.Locators.NAME, "name")
        d1,d2=mock.Mock(), mock.Mock()
        p1,p2=p(d1, "http://p1"),p(d2, "http://p2")
        e1,e2=mock.Mock(), mock.Mock()
        e2.tag_name = e1.tag_name = "div"
        e1.text = "t1"
        e2.text = "t2"
        d1.find_element.return_value = e1
        d2.find_element.return_value = e2
        self.assertEqual(p1.el.text,"t1")
        self.assertEqual(p2.el.text,"t2")
        self.assertEqual(d1.get.call_count, 1)
        self.assertEqual(d2.get.call_count, 1)
    def test_multiple_pageinstances_multithreaded(self):
        """ https://github.com/alisaifee/holmium.core/issues/4
        """
        class p(holmium.core.Page):
            el = holmium.core.Element(holmium.core.Locators.NAME, "name")
        class p2(holmium.core.Page):
            el = holmium.core.Element(holmium.core.Locators.NAME, "name")

        def exec_page_in_thread(p):
            p.go_home()
            self.assertEqual(p.t, p.el.text)
            self.assertEqual(p.driver.get.call_count, 2)

        def build_pages(po):
            pages=[]
            for i in range(0,100):
                d = mock.Mock()
                e = mock.Mock()
                e.text = str(p)+str(i)
                e.tag = "div"
                d.find_element.return_value = e
                _p = po(d,"http://%s" % i)
                _p.t = str(p)+str(i)
                pages.append(_p)
            return pages
        pages = build_pages(p)
        pages.extend(build_pages(p2))

        threads = [threading.Thread(target=exec_page_in_thread, args=(p,)) for p in pages]
        [k.start() for k in threads]
        [k.join() for k in threads]

    def test_fluent_response(self):
        """ https://github.com/alisaifee/holmium.core/issues/8
        """
        class p(holmium.core.Page):
            el = holmium.core.Element(holmium.core.Locators.NAME, "name")
            def f1(self):
                self.el.click()
            def f2(self):
                return False
            def f3(self):
                return []
            def f4(self):
                return {}
            def f5(self):
                return ""
        d1=mock.Mock()
        p1=p(d1, "http://p1")
        self.assertEqual(p1, p1.f1())
        self.assertEqual(False, p1.f2())
        self.assertEqual([], p1.f3())
        self.assertEqual({}, p1.f4())
        self.assertEqual("",p1.f5())

