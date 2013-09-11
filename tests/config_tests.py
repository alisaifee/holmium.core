import unittest
from holmium.core import Config
import json
import os

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
        self.assertEquals(cfg["t1"], u"1")
        self.assertEquals(cfg["t2"], 3)
        self.assertEquals(cfg["t3"], 4)
        self.assertEquals(cfg["username"], "developmentuser")
        holmium_vars = {"holmium":{"environment":"production"}}
        cfg = Config(json.loads(json_cfg), holmium_vars)
        self.assertEquals(cfg["t1"], 1)
        self.assertEquals(cfg["t2"], 2)
        self.assertEquals(cfg["t3"], 4)
        self.assertEquals(cfg["username"], "productionuser")


    def test_dict_config(self):
        dct_cfg = {"production":
                {"t2":"{{default['t2']}}", "t3":4},
            "development":
                {"t2":u"{{production['t2']}}"},
            "default":
            {"t1":1,"t2":2,"t3":[1,2,3]}}
        cfg = Config(dct_cfg)
        self.assertEquals(cfg["t1"], 1)
        self.assertEquals(cfg["t2"], u"2")
        self.assertEquals(cfg["t3"], [1,2,3])
        holmium_vars = {"holmium":{"environment":"production"}}
        cfg = Config(dct_cfg, holmium_vars)
        self.assertEquals(cfg["t1"], 1)
        self.assertEquals(cfg["t2"], u"2")
        self.assertEquals(cfg["t3"], 4)

    def test_config_update(self):
        cfg = Config({})
        cfg["foo"] = "{{holmium.environment}}"
        cfg["bar"] = 2

        self.assertEquals(cfg["foo"], "development")
        self.assertEquals(cfg["bar"], 2)

    def test_config_defaults_only(self):
        config = {
                "default":{
                    "base_url": "http://{{holmium.environment}}:3000",
                    "registration_url": "{{default.base_url}}/users/sign_up",
                }
            }
        cfg = Config(config)
        self.assertEquals( cfg["registration_url"], u"http://development:3000/users/sign_up")
