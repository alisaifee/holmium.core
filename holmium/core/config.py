"""
configuration objects for holmium
"""
import sys
import os
import inspect

import jinja2
from selenium import webdriver
from selenium.webdriver import FirefoxProfile


class Config(dict):
    """Dictionary like helper class for maintaining test data configurations
    per environment.

:class:`holmium.core.TestCase` and :class:`holmium.core.HolmiumNose` both
look for either a config.json or config.py file in the same directory as the
test file, and will make a ``config`` object available to the test case
instance.

The :class:`holmium.core.Config` object is aware of the environment
(specified with ``--holmium-env`` when using nose or ``HO_ENV`` as an
environment variable) and will return the config variable from that
environment or from the `default` key.

Values in the config file can use :class:`jinja2.Template` templates to access
either values from itself, environment variables or a select magic holmium
variables: ``holmium.environment``, ``holmium.browser``, ``holmium.user_agent``
and ``holmium.remote``.

Example config structure (which uses a magic variable ``holmium.environment``
and an environment variable ``$PATH``).

JSON

.. code-block:: json

    {
            'default': {  'path':"{{PATH}}"
                        , 'login_url': '{{url}}/{{holmium.environment}}/login'}
                        , 'username' : '{{holmium.environment}}user'}
            ,'production': {'url':'http://prod.com'
                            ,'password': 'sekret'}
            ,'development': {'url':'http://dev.com'
                            ,'password': 'password'}
    }

Python

.. code-block:: python

    config = {
        {
            'default': { 'path':"{{PATH}}"
                        , 'login_url': '{{url}}/{{holmium.environment}}/login'}
                        , 'username' : '{{holmium.environment}}user'}
            ,'production': {'url':'http://prod.com'
                            , 'password': 'sekret'}
            ,'development': {'url':'http://dev.com'
                            , 'password': 'password'}
        }
    }

When accessing ``self.config`` within a test, due to the default:

* ``self.config['path']`` will always return the value of the environment
   variable `PATH`,
* ``self.config['password']`` will always return 'sekret'

if ``HO_ENV`` or ``--holmium-env`` are ``production``:

* ``self.config['username']`` will return ``productionuser``
* ``self.config['password']`` will return ``sekret``
* ``self.config['login_url']`` will return ``http://prod.com/production/login``

if ``HO_ENV`` or ``--holmium-env`` are ``development``:

* ``self.config['username']`` will return ``developmentuser``
* ``self.config['password']`` will return ``password``
* ``self.config['login_url']`` will return ``http://dev.com/development/login``

    """

    # pylint: disable=dangerous-default-value
    def __init__(self, dct,
                 environment={"holmium": {"environment": "development"}}):
        self.env = environment
        dict.__init__(self, dct)

    def __getitem__(self, key):
        """
        override to evaluate the values through the template
        """
        def __render(item, context):
            """
            renders the string given the context using the jinja template
            """
            def _check_string_type(_item):
                """
                meh python2/3 stuff.
                """

                if isinstance(_item, str):
                    return True
                elif sys.version_info < (3, 0, 0):
                    if isinstance(_item, eval("unicode")):
                        return True
                return False

            if _check_string_type(item):
                template = jinja2.Template(item)
                rendered = template.render(context)
                if rendered != item:
                    return __render(rendered, context)
                else:
                    return rendered
            else:
                return item

        env_ctx = dict.setdefault(self, self.env["holmium"]["environment"], {})
        default_ctx = dict.setdefault(self, "default", {})
        try:
            item = env_ctx[key]
        except KeyError:
            item = default_ctx[key]

        context = dict(self)
        context.update(os.environ)
        context.update(self.env)
        context.update(default_ctx)
        context.update(env_ctx)
        return __render(item, context)

    def __setitem__(self, key, value):
        """
        override to put the value in the right environment bucket
        """
        sub_dict = dict.setdefault(self, self.env["holmium"]["environment"], {})
        sub_dict[key] = value


BROWSER_MAPPING = {"firefox": webdriver.Firefox,
                   "chrome": webdriver.Chrome,
                   "safari": webdriver.Safari,
                   "ie": webdriver.Ie,
                   "opera": webdriver.Opera,
                   "remote": webdriver.Remote,
                   "phantomjs": webdriver.PhantomJS,
                   "iphone": webdriver.Remote,
                   "ipad": webdriver.Remote,
                   "android": webdriver.Remote}

#:
CAPABILITIES = {"firefox": webdriver.DesiredCapabilities.FIREFOX,
                "chrome": webdriver.DesiredCapabilities.CHROME,
                "safari": webdriver.DesiredCapabilities.SAFARI,
                "ie": webdriver.DesiredCapabilities.INTERNETEXPLORER,
                "opera": webdriver.DesiredCapabilities.OPERA,
                "phantomjs": webdriver.DesiredCapabilities.PHANTOMJS,
                "iphone": webdriver.DesiredCapabilities.IPHONE,
                "ipad": webdriver.DesiredCapabilities.IPAD,
                "android": webdriver.DesiredCapabilities.ANDROID}


class HolmiumConfig(dict):
    """
    utility class for storing holmium configuration options strictly.
    The class behaves like a dictionary after construction
    with the additional behavior that any attributes set on it are available
    as keys in the dictionary and vice versa.
    """
    # pylint: disable=unused-argument,too-many-arguments,star-args
    def __init__(self, browser, remote, capabilities, user_agent, environment,
                 ignore_ssl, fresh_instance):
        data = {}
        for arg in inspect.getargspec(HolmiumConfig.__init__).args[1:]:
            setattr(self, arg, locals()[arg])
            data[arg] = locals()[arg]
        super(HolmiumConfig, self).__init__(**data)


    def __setattr__(self, key, value):
        super(HolmiumConfig, self).__setattr__(key, value)
        super(HolmiumConfig, self).__setitem__(key, value)

    def __setitem__(self, key, value):
        super(HolmiumConfig, self).__setattr__(key, value)
        super(HolmiumConfig, self).__setitem__(key, value)

# pylint: disable=too-few-public-methods
class DriverConfig(object):
    """
    base class for configuring a webdriver
    """

    def __call__(self, config, args):
        return args


class FirefoxConfig(DriverConfig):
    """
    configuration for firefox
    """
    def __call__(self, config, args):
        profile = FirefoxProfile()
        if config.user_agent:
            profile.set_preference("general.useragent.override",
                                   config.user_agent)
        if config.ignore_ssl:
            profile.accept_untrusted_certs = True
        args["firefox_profile"] = profile
        args["capabilities"] = args["desired_capabilities"]
        args.pop("desired_capabilities")
        return args


class ChromeConfig(DriverConfig):
    """
    configuration for chrome
    """
    def __call__(self, config, args):
        args["desired_capabilities"].setdefault("chrome.switches", [])
        if config.user_agent:
            args["desired_capabilities"]["chrome.switches"].append(
                "--user-agent=%s" % config.user_agent)
        if config.ignore_ssl:
            args["desired_capabilities"]["chrome.switches"].append(
                "--ignore-certificate-errors")

        return super(ChromeConfig, self).__call__(config, args)


class PhantomConfig(DriverConfig):
    """
    configuration for phantomjs
    """
    def __call__(self, config, args):
        if config.ignore_ssl:
            args.setdefault("service_args", []).append(
                "--ignore-ssl-errors=true")
        return super(PhantomConfig, self).__call__(config, args)


class RemoteConfig(DriverConfig):
    """
    configuration for remote driver (and anything that doesnt have a
    specific configuration)
    """
    def __call__(self, config, args):
        if config.browser == "firefox":
            if "firefox_profile" in args:
                args["browser_profile"] = args["firefox_profile"]
                args.pop("firefox_profile")
            args["desired_capabilities"] = args["capabilities"]
            args.pop("capabilities")
        args["command_executor"] = config.remote
        return super(RemoteConfig, self).__call__(config, args)


CONFIGURATOR_MAPPER = {
    "firefox": FirefoxConfig(),
    "chrome": ChromeConfig(),
    "phantomjs": PhantomConfig(),
    "remote": RemoteConfig()
}


def configure(config):
    """
    sets up the arguments required by the specific
    :class:`selenium.webdriver.Webdriver` instance
    based on the :class:`holmium.core.config.HolmiumConfig`
    object that is passed in.
    """
    if config.browser not in BROWSER_MAPPING.keys():
        raise RuntimeError("unknown browser %s" % config.browser)
    merged_capabilities = CAPABILITIES[config.browser]
    merged_capabilities.update(config.capabilities)
    args = {"desired_capabilities": merged_capabilities}
    if config.browser in CONFIGURATOR_MAPPER:
        args = CONFIGURATOR_MAPPER[config.browser](config, args)
    if config.remote:
        args = CONFIGURATOR_MAPPER["remote"](config, args)

    return args

