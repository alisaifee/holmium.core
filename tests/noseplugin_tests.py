import unittest
import os
import json
import mock

from nose.plugins import PluginTester
from nose.plugins.skip import Skip

import holmium.core
from holmium.core.env import ENV
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
            , "--holmium-browser-per-test"
            ]
    suitepath = os.path.join(support, 'options')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.BROWSER_MAPPING
        holmium.core.noseplugin.BROWSER_MAPPING = build_mock_mapping("remote")
        holmium.core.noseplugin.BROWSER_MAPPING.update(build_mock_mapping("firefox"))
        ENV.clear()
        super(TestOptionsWithFirefox,self).setUp()
    def runTest(self):
        assert "ERROR" not in self.output, self.output
        assert "FAIL" not in self.output, self.output
    def tearDown(self):
        holmium.core.BROWSER_MAPPING = self.old_mapping

class TestOptionsWithChrome(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=staging'
            , '--holmium-browser=chrome'
            , '--holmium-useragent="test useragent"'
            , '--holmium-remote=http://nowhere.org'
            , "--holmium-capabilities=%s" % json.dumps({"foo":1})
            , "--holmium-ignore-ssl-errors"
            , "--holmium-browser-per-test"
            ]
    suitepath = os.path.join(support, 'options')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.BROWSER_MAPPING
        holmium.core.noseplugin.BROWSER_MAPPING = build_mock_mapping("remote")
        holmium.core.noseplugin.BROWSER_MAPPING.update(build_mock_mapping("chrome"))
        ENV.clear()
        super(TestOptionsWithChrome,self).setUp()
    def runTest(self):
        assert "ERROR" not in self.output, self.output
        assert "FAIL" not in self.output, self.output
    def tearDown(self):
        holmium.core.noseplugin.BROWSER_MAPPING = self.old_mapping

class TestOptionsWithPhantom(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=staging'
        , '--holmium-browser=phantomjs'
        , '--holmium-useragent="test useragent"'
        , '--holmium-remote=http://nowhere.org'
        , "--holmium-capabilities=%s" % json.dumps({"foo":1})
        , "--holmium-ignore-ssl-errors"
        , "--holmium-browser-per-test"
    ]
    suitepath = os.path.join(support, 'options')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.BROWSER_MAPPING
        holmium.core.noseplugin.BROWSER_MAPPING = build_mock_mapping("remote")
        holmium.core.noseplugin.BROWSER_MAPPING.update(build_mock_mapping("phantomjs"))
        ENV.clear()
        super(TestOptionsWithPhantom,self).setUp()
    def runTest(self):
        assert "ERROR" not in self.output, self.output
        assert "FAIL" not in self.output, self.output
    def tearDown(self):
        holmium.core.noseplugin.BROWSER_MAPPING = self.old_mapping

class TestConfigPy(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=tenv'
            , '--holmium-browser=chrome'
            ]
    suitepath = os.path.join(support, 'config_py')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.BROWSER_MAPPING
        holmium.core.noseplugin.BROWSER_MAPPING.update(build_mock_mapping("chrome"))
        ENV.clear()
        super(TestConfigPy,self).setUp()
    def runTest(self):
        assert "ERROR" not in self.output, self.output
        assert "FAIL" not in self.output, self.output
    def tearDown(self):
        holmium.core.noseplugin.BROWSER_MAPPING = self.old_mapping

class TestConfigJson(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=tenv'
            , '--holmium-browser=chrome'
            ]
    suitepath = os.path.join(support, 'config_json')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.BROWSER_MAPPING
        holmium.core.noseplugin.BROWSER_MAPPING.update(build_mock_mapping("chrome"))
        ENV.clear()
        super(TestConfigJson,self).setUp()
    def runTest(self):
        assert "ERROR" not in self.output, self.output
        assert "FAIL" not in self.output, self.output
    def tearDown(self):
        holmium.core.noseplugin.BROWSER_MAPPING = self.old_mapping

class TestConfigBad(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=tenv'
            , '--holmium-browser=chrome'
            ]
    suitepath = os.path.join(support, 'config_bad')
    plugins = [holmium.core.HolmiumNose()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.BROWSER_MAPPING
        holmium.core.noseplugin.BROWSER_MAPPING.update(build_mock_mapping("chrome"))
        ENV.clear()
        super(TestConfigBad,self).setUp()
    def runTest(self):
        assert "ERROR: test_config_bad" in self.output, self.output
    def tearDown(self):
        holmium.core.noseplugin.BROWSER_MAPPING = self.old_mapping

class TestMultipleDriversWithBrowserPerTest(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=tenv'
        , '--holmium-browser=chrome'
        , '--holmium-browser-per-test'
    ]
    suitepath = os.path.join(support, 'multiple_drivers')
    plugins = [holmium.core.HolmiumNose(), Skip()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.BROWSER_MAPPING
        mock_browsers = build_mock_mapping("chrome")
        holmium.core.noseplugin.BROWSER_MAPPING.update(mock_browsers)
        ENV.clear()
        super(TestMultipleDriversWithBrowserPerTest,self).setUp()
    def runTest(self):
        assert "Ran 2 tests" in self.output, self.output
        assert "OK" in self.output, self.output
        self.assertAlmostEqual(holmium.core.noseplugin.BROWSER_MAPPING["chrome"].return_value.quit.call_count, 3)
        self.assertAlmostEqual(holmium.core.noseplugin.BROWSER_MAPPING["chrome"].call_count, 3)

    def tearDown(self):
        holmium.core.noseplugin.BROWSER_MAPPING = self.old_mapping

class TestMultipleDriversWithReusedBrowsers(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=tenv'
        , '--holmium-browser=chrome'
    ]
    suitepath = os.path.join(support, 'multiple_drivers')
    plugins = [holmium.core.HolmiumNose(), Skip()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.BROWSER_MAPPING
        mock_browsers = build_mock_mapping("chrome")
        holmium.core.noseplugin.BROWSER_MAPPING.update(mock_browsers)
        ENV.clear()
        super(TestMultipleDriversWithReusedBrowsers,self).setUp()
    def runTest(self):
        assert "Ran 2 tests" in self.output, self.output
        assert "OK" in self.output, self.output
        self.assertAlmostEqual(holmium.core.noseplugin.BROWSER_MAPPING["chrome"].call_count, 2)

    def tearDown(self):
        holmium.core.noseplugin.BROWSER_MAPPING = self.old_mapping

class TestDriverBroken(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    args = ['--holmium-environment=tenv'
        , '--holmium-browser=chrome'
    ]
    suitepath = os.path.join(support, 'broken_driver')
    plugins = [holmium.core.HolmiumNose(), Skip()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.BROWSER_MAPPING
        mock_browsers = build_mock_mapping("chrome")
        def fake_construct(*a, **k):
            raise Exception("failed to initialize")
        mock_browsers["chrome"].side_effect = fake_construct
        holmium.core.noseplugin.BROWSER_MAPPING.update(mock_browsers)
        ENV.clear()
        super(TestDriverBroken,self).setUp()
    def runTest(self):
        assert "Ran 1 test" in self.output, self.output
        assert "SKIP=1" in self.output, self.output
    def tearDown(self):
        holmium.core.noseplugin.BROWSER_MAPPING = self.old_mapping

class TestNoDriver(PluginTester, unittest.TestCase):
    activate = "--with-holmium"
    suitepath = os.path.join(support, 'broken_driver')
    plugins = [holmium.core.HolmiumNose(), Skip()]
    def setUp(self):
        self.old_mapping = holmium.core.noseplugin.BROWSER_MAPPING
        mock_browsers = build_mock_mapping("chrome")
        holmium.core.noseplugin.BROWSER_MAPPING.update(mock_browsers)
        ENV.clear()
        super(TestNoDriver,self).setUp()
    def runTest(self):
        assert "Ran 1 test" in self.output, self.output
        assert "SKIP=1" in self.output, self.output
    def tearDown(self):
        holmium.core.noseplugin.BROWSER_MAPPING = self.old_mapping
