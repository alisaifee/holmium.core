import atexit
import copy
import sys
from nose.plugins.skip import SkipTest
from holmium.core.config import configure



class LazyWebDriver(object):
    def __init__(self, driver_cls, holmium_config):
        self._driver_cls = driver_cls
        self._holmium_config = holmium_config
        self._instance = None

    def __getattribute__(self, item):
        safe_getter = lambda i: object.__getattribute__(self, i)
        safe_setter = lambda i, v: object.__setattr__(self, i, v)
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            instance = safe_getter("_instance")
            if not instance:
                try:
                    instance = safe_getter("_driver_cls")(**configure(safe_getter("_holmium_config")))
                except:
                    browser = safe_getter("_holmium_config").browser
                    raise SkipTest("unable to initialize %s driver" % browser), None, sys.exc_info()[2]
                object.__getattribute__(self, "_post_create_callback")()
                safe_setter("_instance", instance)

            return getattr(instance, item)

    def __eq__(self, other):
        return other and self._driver_cls == other._driver_cls


    def _post_create_callback(self):
        atexit.register(object.__getattribute__(self, "safe_quit"))

    def safe_quit(self):
        try:
            instance = object.__getattribute__(self, "_instance")
            if instance:
                instance.quit()
        except SkipTest:  # pragma: no cover
            # absorb since safe_quit is called by holmium itself
            pass  # pragma: no cover
        finally:
            object.__setattr__(self, "_instance", None)

    def safe_clear(self):
        try:
            self.delete_all_cookies()
        except SkipTest:  # pragma: no cover
            # absorb since safe_quit is called by holmium itself
            pass  # pragma: no cover

class LazyWebDriverList(list):
    def __init__(self, *a, **k):
        # reserve idx == 0
        list.__init__(self, *a, **k)
        self.append(0)

    def __getitem__(self, item):
        if item==0:
            return Env.get("driver", None)
        try:
            return list.__getitem__(self, item)
        except IndexError:
            # copy the driver[0]
            if Env.get("driver", None):
                _d = copy.copy(Env["driver"])
                _d._instance = None
                self.insert(item, _d)
                return _d
            return None # pragma: no cover
    def __iter__(self):
        yield Env["driver"]
        for item in self[1:]:
            yield item
Env = {}
