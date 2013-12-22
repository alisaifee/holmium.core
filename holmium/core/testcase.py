"""
the testcase base class
"""
import unittest
import inspect
import imp
import json
import os
from .config import HolmiumConfig, Config, BROWSER_MAPPING
from .env import ENV
from .env import LazyWebDriver, LazyWebDriverList
from nose.plugins.skip import SkipTest

# pylint: disable=too-many-public-methods

class TestCase(unittest.TestCase):
    """
    Base class for creating test classes for writing holmium driven
    test cases. More details can be found at :ref:`testing-unittest`
    """

    @classmethod
    def setUpClass(cls):
        """
        prepare the driver initialization based on the environment variables
        that have been set. The driver is not actually initialized until the
        test itself actually refers to it via `self.driver`.
        """
        cls.driver = None
        base_file = inspect.getfile(cls)
        config_path = os.path.join(os.path.split(base_file)[0], "config")
        browser = os.environ.get("HO_BROWSER", "firefox")
        user_agent = os.environ.get("HO_USERAGENT", "")
        remote = os.environ.get("HO_REMOTE", None)
        environment = os.environ.get("HO_ENV", "development")
        ignore_ssl = os.environ.get("HO_IGNORE_SSL_ERRORS", False)
        fresh_instance = bool(int(os.environ.get("HO_BROWSER_PER_TEST", 0)))
        cls.holmium_config = HolmiumConfig(browser, remote, {}, user_agent,
                                       environment, ignore_ssl, fresh_instance)
        config = None
        if os.path.isfile(config_path + ".json"):
            config = json.loads(open(config_path + ".json").read())
        elif os.path.isfile(config_path + ".py"):
            config = imp.load_source("config", config_path + ".py").config
        if config:
            cls.config = Config(config, {"holmium": cls.holmium_config})
        # pylint: disable=no-member
        if remote:
            driver_cls = BROWSER_MAPPING["remote"]
        else:
            if not cls.holmium_config.browser in BROWSER_MAPPING:
                raise SkipTest("Unknown browser (%s) specified in HO_BROWSER"
                    % ( cls.holmium_config.browser)
                )
            driver_cls = BROWSER_MAPPING[cls.holmium_config.browser]
        cls.driver = ENV.setdefault("driver", LazyWebDriver(driver_cls,
                                                            cls.holmium_config)
        )
        cls.drivers = ENV.setdefault("drivers", LazyWebDriverList())
        if hasattr(super(TestCase, cls), "setUpClass"):
            super(TestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        quit the driver after the test run (or after all the test methods
        in the class have finished if ``HO_BROWSER_PER_TEST`` is set).
        """
        # pylint:disable=no-member
        if ENV.get("driver", None) and cls.holmium_config.fresh_instance:
            for driver in ENV["drivers"]:
                driver.safe_quit()
        if hasattr(super(TestCase, cls), "tearDownClass"):
            super(TestCase, cls).tearDownClass()

    def tearDown(self):
        """
        clear the cookies on the driver after each test
        """
        if ENV.get("driver", None):
            for driver in ENV["drivers"]:
                driver.safe_clear()
        super(TestCase, self).tearDown()


    # helper assertions
    # pylint: disable=invalid-name
    def assertElementTextEqual(self, element, text, msg=None):
        """
        Fail if the text attribute of the element does not match
        """
        self.assertEqual(element.text, text, msg)

    def assertElementAttributeEqual(self, element, key, value, msg=None):
        """
        Fail if the element does not have the specified attribute value
        """
        self.assertEqual(element.get_attribute(key), value, msg)

    def assertElementDisplayed(self, element, msg=None):
        """
        Fail if the element is not visible
        """
        self.assertTrue(element.is_displayed(), msg)

    def assertElementsDisplayed(self, elements, msg=None):
        """
        Fail if any of the elements in the element collection are not
        visible
        """
        _ = elements.values() if isinstance(elements, dict) else elements
        self.assertTrue(all((el.is_displayed() for el in _)), msg)

    def assertElementCSS(self, element, css_property, value, msg=None):
        # pylint:disable=line-too-long
        """
        Fail if the element does not exhibit the correct css property value.
        The value of the elements css property is the one returned by
        :meth:`selenium.webdriver.remote.webelement.WebElement.value_of_css_property`
        """
        self.assertEqual(element.value_of_css_property(css_property),
                         value,
                         msg
        )

    def assertElementSize(self, element,  width, height, msg=None):
        """ Fail if the element size does not match the provided values
        """
        _expected = {"height":height, "width":width}
        self.assertEqual(_expected, element.size, msg)

