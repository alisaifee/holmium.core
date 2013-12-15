import unittest
import os

import mock
from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest

from holmium.core import TestCase, Element, Elements, ElementMap, Locators
from holmium.core.env import ENV
import holmium.core.testcase

from .utils import mock_open, build_mock_mapping


def runtc(env, validations):
    try:
        _pre_env = dict(os.environ)
        os.environ.update(env)
        class t1(TestCase):
            def runTest(self):
                self.driver.get("http://nowhere.org")
                for validation in validations:
                    self.assertTrue(validation(self))
        test = t1()
        test.setUpClass()
        test.setUp()
        test.runTest()
        test.tearDown()
        test.tearDownClass()
    finally:
        os.environ = _pre_env

def runtc2drivers(env, validations):
    try:
        _pre_env = dict(os.environ)
        os.environ.update(env)
        class t2(TestCase):
            def runTest(self):
                self.driver.get("http://nowhere.org")
                self.drivers[0].get("http://nowhere.org")
                self.drivers[1].get("http://nowhere.org")
                for validation in validations:
                    self.assertTrue(validation(self))
        test = t2()
        test.setUpClass()
        test.setUp()
        test.runTest()
        test.tearDown()
        test.tearDownClass()
    finally:
        os.environ = _pre_env

class TestCaseTests(unittest.TestCase):
    def setUp(self):
        if ENV.has_key("driver"):
            ENV.pop("driver")

    def test_set_browser(self):
        with mock.patch.dict('holmium.core.testcase.BROWSER_MAPPING', build_mock_mapping("phantomjs")):
            runtc({"HO_BROWSER":"phantomjs"}, [lambda s:s.driver!=None])

    def test_set_browser_phantom(self):
        with mock.patch.dict('holmium.core.testcase.BROWSER_MAPPING', build_mock_mapping("phantomjs")):
            runtc({"HO_BROWSER":"phantomjs"}, [lambda s:s.driver!=None, lambda s:s.driver.name == "phantomjs"])

    def test_set_browser_remote(self):
        with mock.patch.dict('holmium.core.testcase.BROWSER_MAPPING', build_mock_mapping("remote")):
            runtc({"HO_BROWSER":"phantomjs", "HO_REMOTE":"http://lala.com"}, [lambda s:s.driver!=None, lambda s:s.driver.name == "remote"])

    def test_auto_config_json(self):
        with mock.patch("os.path.isfile") as isfile:
            with mock.patch.dict('holmium.core.testcase.BROWSER_MAPPING', build_mock_mapping("phantomjs")):
                isfile.side_effect = lambda name:name.find("json")>0
                with mock_open() as op:
                    op.return_value.read.return_value = '{"default": {"test": 1}}'
                    runtc({"HO_BROWSER":"phantomjs"}, [lambda s:s.config["test"]==1])

    def test_auto_config_py(self):
        with mock.patch("os.path.isfile") as isfile:
            with mock.patch.dict('holmium.core.testcase.BROWSER_MAPPING', build_mock_mapping("phantomjs")):
                isfile.side_effect = lambda name:name.find("py")>0
                with mock.patch("imp.load_source") as load_source:
                    m_config = mock.Mock()
                    m_config.config = {"default":{"test":1}}
                    load_source.return_value = m_config
                    runtc({"HO_BROWSER":"phantomjs"}, [lambda s:s.config["test"]==1])

    def test_set_useragent(self):
        with mock.patch.dict('holmium.core.testcase.BROWSER_MAPPING', build_mock_mapping("firefox")):
            runtc({"HO_BROWSER":"firefox", "HO_USERAGENT":"holmium.core"}, [])
            call_args = holmium.core.testcase.BROWSER_MAPPING["firefox"].call_args
            assert len(call_args) == 2
            assert "firefox_profile" in call_args[1]
            ff_profile = call_args[1]["firefox_profile"]
            ua = ff_profile.default_preferences["general.useragent.override"]
            self.assertEqual(ua, 'holmium.core')

    def test_invalid_browser(self):
        self.assertRaises(SkipTest, runtc, {"HO_BROWSER":"direfox", "HO_BROWSER_PER_TEST":"1"}, [])

    def test_browser_per_test(self):
        with mock.patch.dict('holmium.core.testcase.BROWSER_MAPPING', build_mock_mapping("firefox")):
            runtc({"HO_BROWSER":"firefox", "HO_BROWSER_PER_TEST":"1"}, [])
            self.assertEquals(holmium.core.testcase.BROWSER_MAPPING["firefox"].return_value.quit.call_count, 1)
        ENV.clear()
        with mock.patch.dict('holmium.core.testcase.BROWSER_MAPPING', build_mock_mapping("firefox")):
            runtc({"HO_BROWSER":"firefox", "HO_BROWSER_PER_TEST":"0"}, [])
            self.assertEquals(holmium.core.testcase.BROWSER_MAPPING["firefox"].return_value.quit.call_count, 0)

    def test_multiple_browser_per_test(self):
        with mock.patch.dict('holmium.core.testcase.BROWSER_MAPPING', build_mock_mapping("firefox")):
            runtc2drivers({"HO_BROWSER":"firefox", "HO_BROWSER_PER_TEST":"0"}, [])
            self.assertEquals(holmium.core.testcase.BROWSER_MAPPING["firefox"].call_count, 2)
        ENV.clear()
        with mock.patch.dict('holmium.core.testcase.BROWSER_MAPPING', build_mock_mapping("firefox")):
            runtc2drivers({"HO_BROWSER":"firefox", "HO_BROWSER_PER_TEST":"1"}, [])
            self.assertEquals(holmium.core.testcase.BROWSER_MAPPING["firefox"].call_count, 2)
            self.assertEquals(holmium.core.testcase.BROWSER_MAPPING["firefox"].return_value.quit.call_count, 2)

