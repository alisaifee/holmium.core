import os
import unittest
from selenium import webdriver
import inspect
import imp
import holmium

browser_mapping = {"firefox": webdriver.Firefox,
                    "chrome": webdriver.Chrome,
                    "ie": webdriver.Ie,
                    "opera" : webdriver.Opera,
                    "remote": webdriver.Remote}

#:
capabilities = {"firefox": webdriver.DesiredCapabilities.FIREFOX,
                "chrome": webdriver.DesiredCapabilities.CHROME,
                "ie": webdriver.DesiredCapabilities.INTERNETEXPLORER,
                "opera": webdriver.DesiredCapabilities.OPERA}


class HolmiumTestCase(unittest.TestCase):
    """
    """
    #:
    @classmethod
    def setUp(self):
        """
        """
        pass

    @classmethod
    def setUpClass(self):
        """
        """
        self.driver = None
        base_file = inspect.getfile(self)
        config_path = os.path.join(os.path.split(base_file)[0], "config.py")
        try:
            config = imp.load_source("config", config_path)
            self.config = config.config[os.environ.get("HO_ENV", "prod")]
        except IOError:
            holmium.core.log.debug("config.py not found for TestClass %s at %s" %
                                           (self, config_path))

        driver = os.environ.get("HO_BROWSER", "firefox").lower()
        remote_url = os.environ.get("HO_REMOTE", "").lower()
        args = {}
        if remote_url:
            cap = capabilities[driver]
            args = {"command_executor": remote_url,
                     "desired_capabilities": cap}
            driver = "remote"
        self.driver = browser_mapping[driver](**args)

    @classmethod
    def tearDownClass(self):
        if self.driver:
            self.driver.quit()

    @classmethod
    def tearDown(self):
        """
        """
        if self.driver:
            self.driver.delete_all_cookies()
