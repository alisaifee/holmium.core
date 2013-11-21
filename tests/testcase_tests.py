import unittest
import os

import mock

import holmium.core
import holmium.core.config


def runtc(env, validations):
    try:
        _pre_env = dict(os.environ)
        os.environ.update(env)
        class t(holmium.core.TestCase):
            def runTest(self):
                for validation in validations:
                    self.assertTrue(validation(self))

        test = t()
        test.setUpClass()
        test.setUp()
        test.runTest()
        test.tearDown()
        test.tearDownClass()
    finally:
        os.environ = _pre_env

def build_mock_mapping(name):
    mock_driver = mock.Mock()
    browser_mapping = {name:mock_driver}
    mock_driver.return_value.name = name
    return browser_mapping

class TestCaseTests(unittest.TestCase):
    def test_set_browser(self):
        with mock.patch.dict('holmium.core.config.browser_mapping', build_mock_mapping("phantomjs")):
            runtc({"HO_BROWSER":"phantomjs"}, [lambda s:s.driver!=None])

    def test_set_browser_phantom(self):
        with mock.patch.dict('holmium.core.config.browser_mapping', build_mock_mapping("phantomjs")):
            runtc({"HO_BROWSER":"phantomjs"}, [lambda s:s.driver!=None, lambda s:s.driver.name == "phantomjs"])

    def test_set_browser_remote(self):
        with mock.patch.dict('holmium.core.config.browser_mapping', build_mock_mapping("remote")):
            runtc({"HO_BROWSER":"phantomjs", "HO_REMOTE":"http://lala.com"}, [lambda s:s.driver!=None, lambda s:s.driver.name == "remote"])

    def test_auto_config_json(self):
        with mock.patch("os.path.isfile") as isfile:
            with mock.patch.dict('holmium.core.config.browser_mapping', build_mock_mapping("phantomjs")):
                isfile.side_effect = lambda name:name.find("json")>0
                with mock.patch("__builtin__.open") as op:
                    op.return_value.read.return_value = '{"default": {"test": 1}}'
                    runtc({"HO_BROWSER":"phantomjs"}, [lambda s:s.config["test"]==1])

    def test_auto_config_py(self):
        with mock.patch("os.path.isfile") as isfile:
            with mock.patch.dict('holmium.core.config.browser_mapping', build_mock_mapping("phantomjs")):
                isfile.side_effect = lambda name:name.find("py")>0
                with mock.patch("imp.load_source") as load_source:
                    m_config = mock.Mock()
                    m_config.config = {"default":{"test":1}}
                    load_source.return_value = m_config
                    runtc({"HO_BROWSER":"phantomjs"}, [lambda s:s.config["test"]==1])

    def test_set_useragent(self):
        with mock.patch.dict('holmium.core.config.browser_mapping', build_mock_mapping("firefox")):
            runtc({"HO_BROWSER":"firefox", "HO_USERAGENT":"holmium.core"}, [])
            call_args = holmium.core.config.browser_mapping["firefox"].call_args
            assert len(call_args) == 2
            assert call_args[1].has_key("firefox_profile")
            ff_profile = call_args[1]["firefox_profile"]
            ua = ff_profile.default_preferences["general.useragent.override"]
            self.assertEquals(ua, '"holmium.core"')
