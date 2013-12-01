import unittest
import inspect
import imp
import json

import os
from .config import HolmiumConfig, configure, Config, browser_mapping


class TestCase(unittest.TestCase):
    """
    Base class for creating test classes for writing holmium driven
    test cases. More details can be found at :ref:`testing-unittest`.
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
        super(TestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        quit the driver after all the test methods in the class have
        finished.
        """
        if cls.driver:
            cls.driver.quit()
        super(TestCase, cls).tearDownClass()

    def tearDown(self):
        """
        clear the cookies on the driver after each test
        """
        if hasattr(self, "driver"):
            self.driver.delete_all_cookies()
        super(TestCase,self).tearDown()
