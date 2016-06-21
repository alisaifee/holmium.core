import unittest
import json

from holmium.core import Config
from holmium.core.config import HolmiumConfig, configure


class ConfigTests(unittest.TestCase):
    def test_json_config(self):
        json_cfg = """
    {
        "default": {
            "t3": 4,
            "username":"{{holmium.environment}}user"
        },
        "production":
        {
            "t1": 1,
            "t2": 2
        },
        "development":
        {
            "t1": "{{production['t1']}}",
            "t2": 3
        }
    }
    """
        cfg = Config(json.loads(json_cfg))
        self.assertEqual(cfg["t1"], u"1")
        self.assertEqual(cfg["t2"], 3)
        self.assertEqual(cfg["t3"], 4)
        self.assertEqual(cfg["username"], "developmentuser")
        holmium_vars = {"holmium":{"environment":"production"}}
        cfg = Config(json.loads(json_cfg), holmium_vars)
        self.assertEqual(cfg["t1"], 1)
        self.assertEqual(cfg["t2"], 2)
        self.assertEqual(cfg["t3"], 4)
        self.assertEqual(cfg["username"], "productionuser")


    def test_dict_config(self):
        dct_cfg = {"production":
                {"t2":"{{default['t2']}}", "t3":4},
            "development":
                {"t2":u"{{production['t2']}}"},
            "default":
            {"t1":1,"t2":2,"t3":[1,2,3]}}
        cfg = Config(dct_cfg)
        self.assertEqual(cfg["t1"], 1)
        self.assertEqual(cfg["t2"], u"2")
        self.assertEqual(cfg["t3"], [1,2,3])
        holmium_vars = {"holmium":{"environment":"production"}}
        cfg = Config(dct_cfg, holmium_vars)
        self.assertEqual(cfg["t1"], 1)
        self.assertEqual(cfg["t2"], u"2")
        self.assertEqual(cfg["t3"], 4)

    def test_config_update(self):
        cfg = Config({})
        cfg["foo"] = "{{holmium.environment}}"
        cfg["bar"] = 2

        self.assertEqual(cfg["foo"], "development")
        self.assertEqual(cfg["bar"], 2)

    def test_config_defaults_only(self):
        config = {
                "default":{
                    "base_url": "http://{{holmium.environment}}:3000",
                    "registration_url": "{{default.base_url}}/users/sign_up",
                }
            }
        cfg = Config(config)
        self.assertEqual( cfg["registration_url"], u"http://development:3000/users/sign_up")

    def test_config_default_reference(self):
        config = {
                "default":{
                    "base_url": "http://{{holmium.environment}}:3000",
                    "registration_url": "{{base_url}}/users/sign_up",
                    "random_var":"{{env_random}}"
                },
                "production":{
                    "base_url": "http://awesomesite.com",
                    "env_random":"1",
                    "extended_random": "random_{{random_var}}"
                }
            }
        holmium_vars = {"holmium":{"environment":"production"}}
        cfg = Config(config, holmium_vars)
        self.assertEqual( cfg["registration_url"], u"http://awesomesite.com/users/sign_up")
        self.assertEqual( cfg["extended_random"], u"random_1")
        cfg = Config(config)
        self.assertEqual( cfg["registration_url"], u"http://development:3000/users/sign_up")

    def test_holmium_config_object(self):

        cfg = HolmiumConfig(1,2,3,4,5,6,7,8)
        self.assertEqual(cfg,  {
            "browser":1,
            "remote":2,
            "capabilities":3,
            "config_dir":4,
            "user_agent":5,
            "environment":6,
            "ignore_ssl":7,
            "fresh_instance":8,
        })

        self.assertEqual(cfg.browser, 1)
        self.assertEqual(cfg.remote, 2)
        self.assertEqual(cfg.capabilities, 3)
        self.assertEqual(cfg.config_dir, 4)
        self.assertEqual(cfg.user_agent, 5)
        self.assertEqual(cfg.environment, 6)
        self.assertEqual(cfg.ignore_ssl, 7)
        self.assertEqual(cfg.fresh_instance, 8)

        cfg.browser = 2
        self.assertEqual(cfg.browser, 2)
        self.assertEqual(cfg["browser"],2)

        nested = {"holmium":{}}
        nested["holmium"]["config"] = cfg
        nested["holmium"]["config"]["user_agent"] = 1
        self.assertEqual(cfg.user_agent , 1)

        cfg["foo"] = "bar"
        self.assertEqual(cfg.foo, "bar")

    def test_holmium_config_unknown_browser(self):
        cfg = HolmiumConfig(
            "awesome",
            "",
            {},
            ".",
            "",
            "development",
            False,
            False
        )
        self.assertRaises(RuntimeError, configure, cfg)
