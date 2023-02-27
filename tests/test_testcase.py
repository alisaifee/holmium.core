import os
import unittest

import mock
from nose.plugins.skip import SkipTest

import holmium.core.testcase
from holmium.core import TestCase
from holmium.core.env import ENV

from .utils import build_mock_mapping, mock_open


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
        if "driver" in ENV:
            ENV.pop("driver")

    def test_set_browser(self):
        with mock.patch.dict(
            "holmium.core.testcase.BROWSER_MAPPING", build_mock_mapping("chrome")
        ):
            runtc({"HO_BROWSER": "chrome"}, [lambda s: s.driver is not None])

    def test_set_browser_phantom(self):
        with mock.patch.dict(
            "holmium.core.testcase.BROWSER_MAPPING", build_mock_mapping("chrome")
        ):
            runtc(
                {"HO_BROWSER": "chrome"},
                [
                    lambda s: s.driver is not None,
                    lambda s: s.driver.name == "chrome",
                ],
            )

    def test_set_browser_remote(self):
        with mock.patch.dict(
            "holmium.core.testcase.BROWSER_MAPPING", build_mock_mapping("remote")
        ):
            runtc(
                {"HO_BROWSER": "chrome", "HO_REMOTE": "http://lala.com"},
                [lambda s: s.driver is not None, lambda s: s.driver.name == "remote"],
            )

    def test_auto_config_json(self):
        with mock.patch("os.path.isfile") as isfile:
            with mock.patch.dict(
                "holmium.core.testcase.BROWSER_MAPPING", build_mock_mapping("chrome")
            ):
                isfile.side_effect = lambda name: name.find("json") > 0
                with mock_open() as op:
                    op.return_value.read.return_value = (
                        '{"default": {"test": 1}}'  # noqa: E501
                    )
                    runtc({"HO_BROWSER": "chrome"}, [lambda s: s.config["test"] == 1])

    def test_auto_config_py(self):
        with mock.patch("os.path.isfile") as isfile:
            with mock.patch.dict(
                "holmium.core.testcase.BROWSER_MAPPING", build_mock_mapping("chrome")
            ):
                isfile.side_effect = lambda name: name.find("py") > 0
                with mock.patch("imp.load_source") as load_source:
                    m_config = mock.Mock()
                    m_config.config = {"default": {"test": 1}}
                    load_source.return_value = m_config
                    runtc({"HO_BROWSER": "chrome"}, [lambda s: s.config["test"] == 1])

    def test_set_useragent(self):
        with mock.patch.dict(
            "holmium.core.testcase.BROWSER_MAPPING", build_mock_mapping("firefox")
        ):
            runtc({"HO_BROWSER": "firefox", "HO_USERAGENT": "holmium.core"}, [])
            call_args = holmium.core.testcase.BROWSER_MAPPING[
                "firefox"
            ].call_args  # noqa: E501
            assert len(call_args) == 2
            assert "firefox_profile" in call_args[1]
            ff_profile = call_args[1]["firefox_profile"]
            ua = ff_profile.default_preferences["general.useragent.override"]
            self.assertEqual(ua, "holmium.core")

    def test_invalid_browser(self):
        self.assertRaises(
            SkipTest, runtc, {"HO_BROWSER": "direfox", "HO_BROWSER_PER_TEST": "1"}, []
        )

    def test_browser_per_test(self):
        with mock.patch.dict(
            "holmium.core.testcase.BROWSER_MAPPING", build_mock_mapping("firefox")
        ):
            runtc({"HO_BROWSER": "firefox", "HO_BROWSER_PER_TEST": "1"}, [])
            self.assertEquals(
                holmium.core.testcase.BROWSER_MAPPING[
                    "firefox"
                ].return_value.quit.call_count,
                1,  # noqa: E501
            )
        ENV.clear()
        with mock.patch.dict(
            "holmium.core.testcase.BROWSER_MAPPING", build_mock_mapping("firefox")
        ):
            runtc({"HO_BROWSER": "firefox", "HO_BROWSER_PER_TEST": "0"}, [])
            self.assertEquals(
                holmium.core.testcase.BROWSER_MAPPING[
                    "firefox"
                ].return_value.quit.call_count,  # noqa: E501
                0,
            )

    def test_multiple_browser_per_test(self):
        with mock.patch.dict(
            "holmium.core.testcase.BROWSER_MAPPING", build_mock_mapping("firefox")
        ):
            runtc2drivers({"HO_BROWSER": "firefox", "HO_BROWSER_PER_TEST": "0"}, [])
            self.assertEquals(
                holmium.core.testcase.BROWSER_MAPPING["firefox"].call_count, 2
            )
        ENV.clear()
        with mock.patch.dict(
            "holmium.core.testcase.BROWSER_MAPPING", build_mock_mapping("firefox")
        ):
            runtc2drivers({"HO_BROWSER": "firefox", "HO_BROWSER_PER_TEST": "1"}, [])
            self.assertEquals(
                holmium.core.testcase.BROWSER_MAPPING["firefox"].call_count, 2
            )
            self.assertEquals(
                holmium.core.testcase.BROWSER_MAPPING[
                    "firefox"
                ].return_value.quit.call_count,  # noqa: E501
                2,
            )
