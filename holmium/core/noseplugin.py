import imp
import os
import json
from nose.plugins.base import Plugin
from nose.plugins.skip import SkipTest
import holmium.core
import selenium.webdriver

class HolmiumNose(Plugin):
    """
    nose plugin to allow bootstrapping testcases with a selenium driver
    """
    name = "holmium"
    enabled = False


    def __init__(self):
        Plugin.__init__(self)
        self.driver = None
        self.config = {} 
        self.environment = None
        self.driver_initializer_fn = lambda _:None
        self.logger = holmium.core.log

    def options(self, parser, env):
        """
        Register command line options
        """
        parser.add_option("", "--with-holmium", dest="ho_enabled", action="store_true", help="use holmium to setup test case environment")
        parser.add_option("", "--holmium-environment", dest="ho_env", help = "environment to pass to holmium test case configuration")
        parser.add_option("", "--holmium-browser", dest="ho_browser", type = "choice", choices = list(holmium.core.browser_mapping.keys()), help="the selenium driver to invoke")
        parser.add_option("", "--holmium-remote", dest="ho_remote", help = "full url to remote selenium instance")
        parser.add_option("", "--holmium-capabilities", dest="ho_cap", help = "json dictionary of extra capabilities")
        parser.add_option("", "--holmium-useragent", dest="ho_ua", help="User-agent string to use. Only available for firefox & chrome")

    def configure( self, options, conf ):
        if options.ho_enabled:
            browser = options.ho_browser or ("HO_BROWSER" in os.environ and os.environ["HO_BROWSER"] )
            self.environment = options.ho_env or ("HO_ENVIRONMENT" in os.environ and os.environ["HO_ENVIRONMENT"])
            remote_url = options.ho_remote or ("HO_REMOTE" in os.environ and os.environ["HO_REMOTE"])
            args = {}
            caps = {}
            if options.ho_ua:
                if browser not in ["chrome","firefox"]:
                    raise SkipTest("useragent string can only be overridden for chrome & firefox")
                else:
                    if browser == "chrome":
                        caps.update({"chrome.switches":["--user-agent=%s" % options.ho_ua]})
                    elif browser == "firefox":
                        ffopts = selenium.webdriver.FirefoxProfile()
                        ffopts.set_preference("general.useragent.override", options.ho_ua)
                        ffopts.update_preferences()
                        if options.ho_remote:
                            args.update({"browser_profile":ffopts})
                        else:
                            args.update({"firefox_profile":ffopts})

            if remote_url:
                caps.update(holmium.core.capabilities[browser])
                args.update( {"command_executor": remote_url,
                        "desired_capabilities": caps})
                browser = "remote"
            if options.ho_cap:
                try:
                    cap = json.loads( options.ho_cap  )
                    if args.has_key("desired_capabilities"):
                        args["desired_capabilities"].update(cap)
                except Exception as e:
                    self.logger.error("unable to load capabilities")
                    raise SkipTest("holmium could not be initialized due to a problem with the provided capabilities " + str(e))
            self.driver_initializer_fn = lambda:holmium.core.browser_mapping[browser](**args)
            self.enabled = True

    def beforeTest(self, test):
        try:
            if not self.driver:
                self.driver = self.driver_initializer_fn()
        except Exception as e:
            self.logger.error("failed to initialize selenium driver %s" % e)
            raise SkipTest("holmium could not be initialized due to a problem with the required selenium driver")
        base_file = test.address()[0]
        config_path = os.path.join(os.path.split(base_file)[0], "config.py")
        try:
            config = imp.load_source("config", config_path)
            self.config = config.config[self.environment]
        except IOError as e:
            self.logger.debug("config.py not found at %s" % config_path)
        except KeyError as e:
            self.logger.warn("unable to find environment %s in %s" % (self.environment, config_path))
        except Exception as e:
            self.logger.exception("unable to load %s" % config_path)
        setattr(test.test, "config", self.config)
    def startTest(self, test):
        if self.driver:
            try:
                setattr(test.test, "driver", self.driver)
                self.driver.delete_all_cookies()
            except Exception as e:
                self.logger.error("error clearing cookies %s" % e)

    def finalize(self, result):
        if self.driver:
            self.driver.quit()

