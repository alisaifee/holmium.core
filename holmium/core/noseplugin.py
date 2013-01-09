import inspect
import imp
import os
from nose.plugins.base import Plugin
from nose.plugins.skip import SkipTest
import holmium.core

class HolmiumNose(Plugin):
    """
    nose plugin to allow bootstrapping testcases with a selenium driver
    """
    name = "holmium"
    enabled = False


    def __init__(self):
        Plugin.__init__(self)
        self.driver = None
        self.environment = None
        self.driver_initializer_fn = lambda _:None
        self.logger = holmium.core.log

    def options(self, parser, env):
        """
        Register command line options
        """
        parser.add_option("", "--with-holmium", dest="ho_enabled", action="store_true", help="use holmium to setup test case environment")
        parser.add_option("", "--holmium-environment", dest="ho_env", help = "environment to pass to holmium test case configuration")
        parser.add_option("", "--holmium-browser", dest="ho_browser", type = "choice", choices = holmium.core.browser_mapping.keys())
        parser.add_option("", "--holmium-remote", dest="ho_remote", help = "full url to remote selenium instance")

    def configure( self, options, conf ):
        if options.ho_enabled:
            browser = options.ho_browser or (os.environ.has_key("HO_BROWSER") and os.environ["HO_BROWSER"] )
            self.environment = options.ho_env or (os.environ.has_key("HO_ENVIRONMENT") and os.environ["HO_ENVIRONMENT"])
            remote_url = options.ho_remote or (os.environ.has_key("HO_REMOTE") and os.environ["HO_REMOTE"])
            args = {}
            if remote_url:
                args.update( {"command_executor": remote_url,
                        "desired_capabilities": holmium.core.capabilities[browser]})
                browser = "remote"

            self.driver_initializer_fn = lambda:holmium.core.browser_mapping[browser](**args)
            self.enabled = True

    def beforeTest(self, test):
        try:
            if not self.driver:
                self.driver = self.driver_initializer_fn()
        except Exception, e:
            self.logger.error("failed to initialize selenium driver %s" % e)
            raise SkipTest("holmium could not be initialized due to a problem with the required selenium driver")
        base_file = test.address()[0]
        config_path = os.path.join(os.path.split(base_file)[0], "config.py")
        try:
            config = imp.load_source("config", config_path)
            setattr(test.test, "config",  config.config[self.environment])
        except Exception, e:
            self.logger.debug("config.py not found for %s" % base_file)

    def startTest(self, test):
        if self.driver:
            try:
                setattr(test.test, "driver", self.driver)
                self.driver.delete_all_cookies()
            except Exception, e:
                self.logger.error("error clearing cookies %s" % e)

    def finalize(self, result):
        if self.driver:
            self.driver.quit()

