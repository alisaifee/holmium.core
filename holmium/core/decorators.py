from functools import wraps


def repeat(loop):
    def __inner(fn):
        @wraps(fn)
        def ___inner(*args, **kwargs):
            ret = None
            for _ in range(0, loop):
                ret = fn(*args, **kwargs)
            return ret
        return ___inner
    return __inner


