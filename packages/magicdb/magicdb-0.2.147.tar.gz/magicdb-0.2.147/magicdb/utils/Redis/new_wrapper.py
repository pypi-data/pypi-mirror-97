import redis

from types import FunctionType
from functools import wraps


def wrapper(method):
    @wraps(method)
    def wrapped(*args, **kwrds):
        print("hi")
        #   ... <do something to/with "method" or the result of calling it>
        print("{!r} executing".format(method.__name__))
        return method(*args, **kwrds)

    return wrapped


class MetaClass(type):
    def __new__(meta, classname, bases, classDict):
        print("UN NEW")
        print(bases[0])
        print(dir(bases))
        newClassDict = {}
        for attributeName, attribute in classDict.items():
            print("attr", attributeName, attribute)
            if isinstance(attribute, FunctionType):
                # replace it with a wrapped version
                attribute = wrapper(attribute)
            newClassDict[attributeName] = attribute
        return type.__new__(meta, classname, bases, newClassDict)


class MyClass(redis.Redis):
    def __getattribute__(self, item):
        print("hi", item)
        return super().__getattribute__(item)


from magicdb.utils.Serverless.span import safe_span


def span(index_of_key: int = 0):
    def add_span(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # add 1 to index of key since 0th index is the redis instance
            args_len = len(args) - 1
            ind = index_of_key + 1
            arg = args[ind] if len(args) > ind else None

            if type(arg) in [dict, list]:
                keys = arg.keys() if type(arg) is dict else arg
                args_len = len(keys)
                if keys:
                    arg = list(keys)[0]

            if len(str(arg)) > 50:
                arg = str(arg)[:50]

            label = f"arg[0]={arg}, len(args)={args_len}"
            with safe_span(label=f"[redis] [{f.__name__}] [{label}]"):
                return f(*args, **kwargs)

        return wrapped

    return add_span


# TODO add sentry to this
def catch_error(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"****REDIS ERROR HERE!**** {f.__name__=}({args=})({kwargs=})", e)
            return None

    return wrapped


class RedisWrapper(redis.Redis):
    @catch_error
    @span(0)
    def get(self, name):
        return super().get(name)

    @catch_error
    @span(0)
    def mget(self, keys, *args):
        return super().mget(keys, *args)

    @catch_error
    @span(0)
    def set(self, name, value, *args, **kwargs):
        return super().set(name, value, *args, **kwargs)

    @catch_error
    @span(0)
    def mset(self, mapping):
        return super().mset(mapping)

    @catch_error
    @span(0)
    def delete(self, *names):
        return super().delete(*names)

    @catch_error
    @span(0)
    def flushdb(self, *args, **kwargs):
        return super().flushdb(*args, **kwargs)

    def pipeline(self, *args, **kwargs):
        pipeline = super().pipeline(*args, **kwargs)
        pipeline.execute = catch_error(span(0)(pipeline.execute))
        return pipeline

    @property
    def r(self):
        return super()


def add_decorators(f):
    return catch_error(span(0)(f))


def pipeline_wrapper(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        pipeline = f(*args, **kwargs)
        pipeline.execute = add_decorators(pipeline.execute)
        return pipeline

    return wrapped


def decorate_redis(r: redis.Redis):
    if getattr(r, "_magic_decorated", False):
        return

    function_names = ["get", "mget", "set", "mset", "delete", "flushdb"]
    for function_name in function_names:
        if f := getattr(r, function_name, None):
            decorated_f = add_decorators(f=f)
            setattr(r, function_name, decorated_f)

    # add pipeline.execute() as well
    if r.pipeline:
        r.pipeline = pipeline_wrapper(r.pipeline)

    setattr(r, "_magic_decorated", True)


import time

if __name__ == "__main__":
    start = time.time()
    r = redis.Redis(
        host="us1-apt-moose-31866.lambda.store",
        port="31866",
        password="7dada21ad5744adc92b0015fdd08cfb1",
    )
    print("took to start", time.time() - start)
    decorate_redis(r)
    # wrapper = MyClass(r)
    # a = wrapper.get("hi")
    setr = r.mset({"hi": "ueee", "yas": "u"})

    r.setex("hi", 40, "2")
    a = r.get("hi")
    print("a", a)
    print("set", setr)
    got = r.mget(["hi", "yas", "d"])
    print("got", got)
    with r.pipeline() as pipe:
        pipe.set("hi", "o")
        pipe.execute()
