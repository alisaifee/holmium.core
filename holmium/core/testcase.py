import unittest
import inspect
import imp
import json

import os
from .config import HolmiumConfig, configure, Config, browser_mapping


class TestCase(unittest.TestCase):
    """
    Base class for creating test classes for writing holmium driven
    test cases. More details can be found at :ref:`testing-unittest`
    """

    @classmethod
    def setUpClass(cls):
        """
        create the driver and configure it before any of the tests run.
        """
        cls.driver = None
        base_file = inspect.getfile(cls)
        config_path = os.path.join(os.path.split(base_file)[0], "config")
        browser = os.environ.get("HO_BROWSER", "firefox")
        user_agent = os.environ.get("HO_USERAGENT", "")
        remote = os.environ.get("HO_REMOTE", None)
        environment = os.environ.get("HO_ENV", "development")
        ignore_ssl = os.environ.get("HO_IGNORE_SSL_ERRORS", False)
        holmium_config = HolmiumConfig(browser, remote, {}, user_agent,
                                       environment, ignore_ssl)
        args = configure(holmium_config)
        config = None
        if os.path.isfile(config_path + ".json"):
            config = json.loads(open(config_path + ".json").read())
        elif os.path.isfile(config_path + ".py"):
            config = imp.load_source("config", config_path + ".py").config
        if config:
            cls.config = Config(config,
                                             {"holmium": holmium_config})
        if remote:
            driver = browser_mapping["remote"]
        else:
            driver = browser_mapping[holmium_config.browser]
        cls.driver = driver(**args)
        if hasattr(super(TestCase, cls), "setUpClass"):
            super(TestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        quit the driver after all the test methods in the class have
        finished.
        """
        if cls.driver:
            cls.driver.quit()
        if hasattr(super(TestCase, cls), "tearDownClass"):
            super(TestCase, cls).tearDownClass()

    def tearDown(self):
        """
        clear the cookies on the driver after each test
        """
        if hasattr(self, "driver"):
            self.driver.delete_all_cookies()
        super(TestCase,self).tearDown()


    # helper assertions

    def assertElementTextEqual(self, element, text, msg=None):
        """ Fail if the text attribute of the element does not match
        """
        self.assertEqual(element.text, text, msg)

    def assertElementDisplayed(self, element, msg=None):
        """ Fail if the element is not visible
        """
        self.assertTrue(element.is_displayed(), msg)

    def assertElementsDisplayed(self, elements, msg=None):
        """ Fail if any of the elements in the element collection are not visible
        """
        _elements = elements.values() if isinstance(elements, dict) else elements
        self.assertTrue(all((el.is_displayed() for el in _elements)), msg)

    def assertElementCSS(self, element, property, value, msg=None):
        """ Fail if the element does not exhibit the correct css property value
        """
        self.assertEqual(element.value_of_css_property(property), value, msg)

    def assertElementSize(self, element,  width, height, msg=None):
        """ Fail if the element size does not match the provided values
        """
        _expected = {"height":height, "width":width}
        self.assertEqual(_expected, element.size, msg)

