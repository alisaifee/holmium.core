import jinja2
import os

class Config(dict):
    """Dictionary like helper class for maintaining test data configurations per environment.

:class:`holmium.core.TestCase` and :class:`holmium.core.HolmiumNose` both
look for either a config.json or config.py file in the same directory as the
test file, and will make a ``config`` object available to the test case instance.

The :class:`holmium.core.Config` object is aware of the environment (specified with ``--holmium-env``
when using nose or ``HO_ENV`` as an environment variable and will return the config variable from that
environment or from the `default` key.

Values in the config file can use :class:`jinja2.Template` templates to access either values from itself, environment variables
or a select magic holmium variables: ``holmium.environment``, ``holmium.browser``, ``holmium.user_agent``
and ``holmium.remote``.

Example config structure (which uses a magic variable ``holmium.environment`` and an environment variable ``$PATH``).

JSON

.. code-block:: json

    {
            'default': { 'url': 'http://localhost'
                        , 'path':"{{PATH}}"
                        , 'login_url': '{{default.url}}/{{holmium.environment}}/login'}
                        , 'username' : '{{holmium.environment}}user'}
            ,'production': {'password': 'sekret'}
            ,'development': {'password': 'password'}
    }

Python

.. code-block:: python

    config = {
        {
            'default': { 'url': 'http://localhost'
                        , 'path':"{{PATH}}"
                        , 'login_url': '{{default.url}}/{{holmium.environment}}/login'}
                        , 'username' : '{{holmium.environment}}user'}
            ,'production': {'password': 'sekret'}
            ,'development': {'password': 'password'}
        }
    }

When accessing ``self.config`` within a test, due to the default:

* ``self.config['path']`` will always return the value of the environment variable `PATH`,
* ``self.config['password']`` will always return 'sekret'
* ``self.config['url']`` will always return 'http://localhost'

if ``HO_ENV`` or ``--holmium-env`` are ``production``:

* ``self.config['username']`` will return ``productionuser``
* ``self.config['password']`` will return ``sekret``
* ``self.config['login_url']`` will return ``http://localhost/production/login``

if ``HO_ENV`` or ``--holmium-env`` are ``development``:

* ``self.config['username']`` will return ``developmentuser``
* ``self.config['password']`` will return ``password``
* ``self.config['login_url']`` will return ``http://localhost/development/login``

    """
    def __init__(self, dct, environment={"holmium":{"environment":"development"}}):
        self.env = environment
        dict.__init__(self, dct)

    def __getitem__(self, key):
        def __render(item, context):
            if issubclass(item.__class__, str) or issubclass(item.__class__,unicode):
                template = jinja2.Template(item)
                rendered = template.render(context)
                if rendered != item:
                    return __render(rendered,context)
                else:
                    return rendered
            else:
                return item
        try:
            item = dict.__getitem__(self, self.env["holmium"]["environment"])[key]
        except KeyError,e:
            item = dict.__getitem__(self, "default")[key]

        context = dict(self)
        context.update(os.environ)
        context.update(self.env)
        return __render(item, context)

    def __setitem__(self, key, value):
        sub_dict = dict.setdefault(self, self.env["holmium"]["environment"], {})
        sub_dict[key] = value

