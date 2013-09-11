import unittest
import holmium.core
import os
import mock
import StringIO

def mk_tc(env, validations):
    os.environ.update(env)
    class t(holmium.core.TestCase):
        def runTest(self):
            for validation in validations:
                self.assertTrue(validation(self))
    return unittest.TestSuite([t()])

def build_mock_mapping(name):
    mock_driver = mock.Mock()
    browser_mapping = {name:mock_driver}
    mock_driver.name = name
    return browser_mapping

def test_set_browser():
    results = unittest.TestResult()
    with mock.patch.dict('holmium.core.browser_mapping', build_mock_mapping("phantomjs")):
        mk_tc({"HO_BROWSER":"phantomjs"}, [lambda self:self.driver!=None]).run(results)
        assert len(results.errors) == 0, results.errors[0][1]

def test_set_browser_phantom():
    results = unittest.TestResult()
    with mock.patch.dict('holmium.core.browser_mapping', build_mock_mapping("phantomjs")):
        mk_tc({"HO_BROWSER":"phantomjs"}, [lambda self:self.driver!=None and self.driver.name == "phantomjs"]).run(results)
        assert len(results.errors) == 0, results.errors[0][1]

def test_auto_config_json():
    results = unittest.TestResult()
    with mock.patch("os.path.isfile") as isfile:
        with mock.patch.dict('holmium.core.browser_mapping', build_mock_mapping("phantomjs")):
            isfile.side_effect = lambda name:name.find("json")>0
            with mock.patch("__builtin__.open") as op:
                op.return_value.read.return_value = '{"default": {"test": 1}}'
                mk_tc({"HO_BROWSER":"phantomjs"}, [lambda self:self.config["test"]!=1]).run(results)
                assert len(results.errors) == 0, results.errors[0][1]

def test_auto_config_py():
    results = unittest.TestResult()
    with mock.patch("os.path.isfile") as isfile:
        with mock.patch.dict('holmium.core.browser_mapping', build_mock_mapping("phantomjs")):
            isfile.side_effect = lambda name:name.find("py")>0
            with mock.patch("imp.load_source") as load_source:
                m_config = mock.Mock()
                m_config.config = {"default":{"test":1}}
                load_source.return_value = m_config
                mk_tc({"HO_BROWSER":"phantomjs"}, [lambda self:self.config["test"]!=1]).run(results)
                assert len(results.errors) == 0, results.errors[0][1]

def test_set_useragent():
    results = unittest.TestResult()
    with mock.patch.dict('holmium.core.browser_mapping', build_mock_mapping("firefox")):
        mk_tc({"HO_BROWSER":"firefox", "HO_USERAGENT":"ali"}, []).run(results)
        assert len(results.errors) == 0, results.errors[0][1]
