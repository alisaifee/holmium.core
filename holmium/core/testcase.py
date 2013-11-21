import os
import unittest
import inspect
import imp
import json

import holmium
from holmium.core.config import HolmiumConfig, configure


class TestCase(unittest.TestCase):
    """
    """

    @classmethod
    def setUpClass(cls):
        """
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
            cls.config = holmium.core.Config(config,
                                             {"holmium": holmium_config})
        if remote:
            driver = holmium.core.config.browser_mapping["remote"]
        else:
            driver = holmium.core.config.browser_mapping[holmium_config.browser]
        print driver
        cls.driver = driver(**args)

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    @classmethod
    def tearDown(cls):
        """
        """
        if cls.driver:
            cls.driver.delete_all_cookies()
