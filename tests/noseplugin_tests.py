import unittest
import holmium.core
from nose.plugins import PluginTester
import mock
import os
import utils
import json
support = os.path.join(os.path.dirname(__file__), "support")

class TestOptionsWithFirefox(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=staging'
            , '--holmium-browser=firefox'
            , '--holmium-useragent="test useragent"'
            , '--holmium-remote=http://nowhere.org'
            , "--holmium-capabilities=%s" % json.dumps({"foo":1})
            ]
    suitepath = os.path.join(support, 'options')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.browser_mapping
        holmium.core.browser_mapping = utils.build_mock_mapping("remote")
        holmium.core.browser_mapping.update(utils.build_mock_mapping("firefox"))
        super(TestOptionsWithFirefox,self).setUp()
    def runTest(self):
        assert "ERROR" not in self.output, self.output
        assert "FAIL" not in self.output, self.output
    def tearDown(self):
        holmium.core.browser_mapping = self.old_mapping

class TestOptionsWithChrome(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=staging'
            , '--holmium-browser=chrome'
            , '--holmium-useragent="test useragent"'
            , '--holmium-remote=http://nowhere.org'
            , "--holmium-capabilities=%s" % json.dumps({"foo":1})
            ]
    suitepath = os.path.join(support, 'options')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.browser_mapping
        holmium.core.browser_mapping = utils.build_mock_mapping("remote")
        holmium.core.browser_mapping.update(utils.build_mock_mapping("chrome"))
        super(TestOptionsWithChrome,self).setUp()
    def runTest(self):
        assert "ERROR" not in self.output, self.output
        assert "FAIL" not in self.output, self.output
    def tearDown(self):
        holmium.core.browser_mapping = self.old_mapping

class TestConfigPy(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=tenv'
            , '--holmium-browser=chrome'
            ]
    suitepath = os.path.join(support, 'config_py')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.browser_mapping
        holmium.core.browser_mapping.update(utils.build_mock_mapping("chrome"))
        super(TestConfigPy,self).setUp()
    def runTest(self):
        assert "ERROR" not in self.output, self.output
        assert "FAIL" not in self.output, self.output
    def tearDown(self):
        holmium.core.browser_mapping = self.old_mapping

class TestConfigJson(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=tenv'
            , '--holmium-browser=chrome'
            ]
    suitepath = os.path.join(support, 'config_json')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.browser_mapping
        holmium.core.browser_mapping.update(utils.build_mock_mapping("chrome"))
        super(TestConfigJson,self).setUp()
    def runTest(self):
        assert "ERROR" not in self.output, self.output
        assert "FAIL" not in self.output, self.output
    def tearDown(self):
        holmium.core.browser_mapping = self.old_mapping
class TestConfigBad(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=tenv'
            , '--holmium-browser=chrome'
            ]
    suitepath = os.path.join(support, 'config_bad')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.browser_mapping
        holmium.core.browser_mapping.update(utils.build_mock_mapping("chrome"))
        super(TestConfigBad,self).setUp()
    def runTest(self):
        assert "ERROR: test_config_bad" in self.output, self.output
    def tearDown(self):
        holmium.core.browser_mapping = self.old_mapping
