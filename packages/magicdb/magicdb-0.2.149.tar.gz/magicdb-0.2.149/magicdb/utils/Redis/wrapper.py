import redis


class RedisWrapper:
    def __init__(self, r: redis.Redis):
        self._r = r

    def __getattr__(self, item, *args, **kwargs):
        func = getattr(self._r, item)
        print("func", func)
        print(f"{args}, {kwargs}")
        return func(*args, **kwargs)


class RedisSuper(redis.Redis):
    def __getattr__(self, item, *args, **kwargs):
        return getattr(super(), item, *args, **kwargs)
        # func = getattr(self._r, item)
        # print("func", func)
        # print(f"{args}, {kwargs}")
        # return func(*args, **kwargs)


from functools import wraps
import inspect


def withx(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        print("decorator")
        x = 1
        f(*args, **kwargs)
        x = 0

    return wrapped


class MyDecoratingBaseClass(object):
    def __init__(self, *args, **kwargs):
        for member in inspect.getmembers(self, predicate=inspect.ismethod):
            if member[0] in self.wrapped_methods:
                setattr(self, member[0], withx(member[1]))


class MyDecoratedSubClass(MyDecoratingBaseClass):
    wrapped_methods = ["a", "b"]

    def a(self):
        print("a")

    def b(self):
        print("b")

    def c(self):
        print("c")


if __name__ == "__main__":
    r = redis.Redis(
        host="us1-apt-moose-31866.lambda.store",
        port="31866",
        password="7dada21ad5744adc92b0015fdd08cfb1",
    )
    wrapper = RedisWrapper(r)
    wrapper.get("hi", "hello")
