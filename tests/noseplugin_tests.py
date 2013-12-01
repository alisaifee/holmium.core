import unittest
import os
import json
import mock

from nose.plugins import PluginTester

import holmium.core
import holmium.core.noseplugin

from .utils import build_mock_mapping

support = os.path.join(os.path.dirname(__file__), "support")

class TestOptionsWithFirefox(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=staging'
            , '--holmium-browser=firefox'
            , '--holmium-useragent="test useragent"'
            , '--holmium-remote=http://nowhere.org'
            , "--holmium-capabilities=%s" % json.dumps({"foo":1})
            , "--holmium-ignore-ssl-errors"
            ]
    suitepath = os.path.join(support, 'options')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.browser_mapping
        holmium.core.noseplugin.browser_mapping = build_mock_mapping("remote")
        holmium.core.noseplugin.browser_mapping.update(build_mock_mapping("firefox"))
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
            , "--holmium-ignore-ssl-errors"
            ]
    suitepath = os.path.join(support, 'options')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.browser_mapping
        holmium.core.noseplugin.browser_mapping = build_mock_mapping("remote")
        holmium.core.noseplugin.browser_mapping.update(build_mock_mapping("chrome"))
        super(TestOptionsWithChrome,self).setUp()
    def runTest(self):
        assert "ERROR" not in self.output, self.output
        assert "FAIL" not in self.output, self.output
    def tearDown(self):
        holmium.core.noseplugin.browser_mapping = self.old_mapping

class TestOptionsWithPhantom(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=staging'
        , '--holmium-browser=phantomjs'
        , '--holmium-useragent="test useragent"'
        , '--holmium-remote=http://nowhere.org'
        , "--holmium-capabilities=%s" % json.dumps({"foo":1})
        , "--holmium-ignore-ssl-errors"
    ]
    suitepath = os.path.join(support, 'options')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.browser_mapping
        holmium.core.noseplugin.browser_mapping = build_mock_mapping("remote")
        holmium.core.noseplugin.browser_mapping.update(build_mock_mapping("phantomjs"))
        super(TestOptionsWithPhantom,self).setUp()
    def runTest(self):
        assert "ERROR" not in self.output, self.output
        assert "FAIL" not in self.output, self.output
    def tearDown(self):
        holmium.core.noseplugin.browser_mapping = self.old_mapping

class TestConfigPy(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=tenv'
            , '--holmium-browser=chrome'
            ]
    suitepath = os.path.join(support, 'config_py')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.browser_mapping
        holmium.core.noseplugin.browser_mapping.update(build_mock_mapping("chrome"))
        super(TestConfigPy,self).setUp()
    def runTest(self):
        assert "ERROR" not in self.output, self.output
        assert "FAIL" not in self.output, self.output
    def tearDown(self):
        holmium.core.noseplugin.browser_mapping = self.old_mapping

class TestConfigJson(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=tenv'
            , '--holmium-browser=chrome'
            ]
    suitepath = os.path.join(support, 'config_json')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.browser_mapping
        holmium.core.noseplugin.browser_mapping.update(build_mock_mapping("chrome"))
        super(TestConfigJson,self).setUp()
    def runTest(self):
        assert "ERROR" not in self.output, self.output
        assert "FAIL" not in self.output, self.output
    def tearDown(self):
        holmium.core.noseplugin.browser_mapping = self.old_mapping

class TestConfigBad(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=tenv'
            , '--holmium-browser=chrome'
            ]
    suitepath = os.path.join(support, 'config_bad')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.browser_mapping
        holmium.core.noseplugin.browser_mapping.update(build_mock_mapping("chrome"))
        super(TestConfigBad,self).setUp()
    def runTest(self):
        assert "ERROR: test_config_bad" in self.output, self.output
    def tearDown(self):
        holmium.core.noseplugin.browser_mapping = self.old_mapping


class TestDriverBroken(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=tenv'
        , '--holmium-browser=chrome'
    ]
    suitepath = os.path.join(support, 'broken_driver')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.browser_mapping
        mock_browsers = build_mock_mapping("chrome")
        self.plugins[0].logger = mock.Mock()
        def fake_construct(*a, **k):
            raise Exception("failed to initialize")
        mock_browsers["chrome"].side_effect = fake_construct
        holmium.core.noseplugin.browser_mapping.update(mock_browsers)
        super(TestDriverBroken,self).setUp()
    def runTest(self):
        assert "Ran 0 tests" in self.output
        assert self.plugins[0].logger.exception.call_count == 1
    def tearDown(self):
        holmium.core.noseplugin.browser_mapping = self.old_mapping
