from contextlib import closing
import os
import sys
import json
from nose.plugins.base import Plugin
from nose.plugins.skip import SkipTest
from .config import HolmiumConfig, Config, browser_mapping
from .env import Env, LazyWebDriverList
from holmium.core.env import LazyWebDriver
from .logger import log

try:
    from fresher import ftc
except ImportError: # pragma: no cover
    ftc = None # pragma: no cover

def load_source(name, path):
    """
    abstracted out for 2.7 versus 3.x support
    """
    if sys.version_info >= (3,0,0):
        from importlib import machinery  # pragma: no cover
        return machinery.SourceFileLoader(name, path).load_module(name)  # pragma: no cover
    else:
        import imp  # pragma: no cover
        return imp.load_source(name, path)  # pragma: no cover

class HolmiumNose(Plugin):
    """
    nose plugin to allow bootstrapping testcases with a selenium driver
    """
    name = "holmium"
    enabled = False


    def __init__(self):
        Plugin.__init__(self)
        self.config = {}
        self.environment = None
        self.logger = log

    def options(self, parser, env):
        """
        Register command line options
        """
        parser.add_option("", "--with-holmium", dest="ho_enabled",
                          action="store_true",
                          help="use holmium to setup test case environment")
        parser.add_option("", "--holmium-environment", dest="ho_env",
                          help="environment to pass to holmium test case configuration")
        parser.add_option("", "--holmium-browser", dest="ho_browser",
                          type="choice",
                          choices=list(
                              browser_mapping.keys()),
                          help="the selenium driver to invoke")
        parser.add_option("", "--holmium-remote", dest="ho_remote",
                          help="full url to remote selenium instance")
        parser.add_option("", "--holmium-capabilities", dest="ho_cap",
                          help="json dictionary of extra capabilities")
        parser.add_option("", "--holmium-useragent", dest="ho_ua",
                          help="User-agent string to use. Only available for firefox & chrome")
        parser.add_option("", "--holmium-ignore-ssl-errors",
                          action="store_true", dest="ho_ignore_ssl",
                          help="Ignore ssl errors while running tests")
        parser.add_option("", "--holmium-browser-per-test",
                          action="store_true", dest="ho_fresh_instance",
                          help="Create a fresh browser per test class",
                          default=False)

    def configure(self, options, conf):
        if options.ho_enabled:
            browser = options.ho_browser or os.environ.get("HO_BROWSER", "")
            environment = options.ho_env or os.environ.get("HO_ENVIRONMENT", "")
            remote_url = options.ho_remote or os.environ.get("HO_REMOTE", "")
            user_agent = options.ho_ua or os.environ.get("HO_USERAGENT", "")
            fresh_instance = options.ho_fresh_instance or bool(int(os.environ.get("HO_BROWSER_PER_TEST",0)))
            ignore_ssl = options.ho_ignore_ssl or os.environ.get(
                "HO_IGNORE_SSL_ERRORS", False)
            caps = options.ho_cap and json.loads(options.ho_cap) or {}

            self.holmium_config = holmium_config = HolmiumConfig(browser,
                                                                 remote_url,
                                                                 caps,
                                                                 user_agent,
                                                                 environment,
                                                                 ignore_ssl,
                                                                 fresh_instance)

            if holmium_config.remote:
                driver_cls = browser_mapping["remote"]
            else:
                driver_cls = browser_mapping[holmium_config.browser]
            self.driver = LazyWebDriver(driver_cls, holmium_config)
            self.enabled = True

    def beforeTest(self, test):
        if not (Env.has_key("driver") and Env["driver"] == self.driver):
            Env["driver"] = self.driver
        if not Env.has_key("drivers"):
            Env["drivers"] = LazyWebDriverList()

        base_file = test.address()[0] if not hasattr(test.test,
                                                     "feature") else test.test.feature.src_file
        config_path = os.path.join(os.path.split(base_file)[0], "config")
        try:
            config = None
            if os.path.isfile(config_path + ".json"):
                with closing(open(config_path + ".json")) as f:
                    config = json.loads(f.read())
            elif os.path.isfile(config_path + ".py"):
                if "holmium_testcase_config" in sys.modules:
                    del sys.modules["holmium_testcase_config"]
                config = load_source("holmium_testcase_config", config_path + ".py").config
            if config:
                self.config = Config(config, {
                "holmium": self.holmium_config})
        except Exception as e:
            self.logger.debug("unable to load %s" % config_path)
            raise SkipTest(
                "error in loading config file at path %s" % config_path, e)
        if HolmiumNose.is_freshen_test(test) and ftc:
            ftc.config = self.config
        else:
            setattr(test.test.__class__, "config", self.config)

    def startTest(self, test):
        if Env.get("driver", None):
            if HolmiumNose.is_freshen_test(test) and ftc:
                ftc.driver = Env["driver"]
                ftc.drivers = Env["drivers"]
            else:
                setattr(test.test.__class__, "driver", Env["driver"])
                setattr(test.test.__class__, "drivers", Env["drivers"])

    def afterTest(self, test):
        if Env.get("driver", None) and self.holmium_config.fresh_instance:
            [_d.safe_quit() for _d in Env["drivers"]]
        elif Env.get("driver"):
            [_d.safe_clear() for _d in Env["drivers"]]

    @staticmethod
    def is_freshen_test(test):
        return test.address()[1] == "fresher.noseplugin"
