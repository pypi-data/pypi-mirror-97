import redis
from functools import wraps


from magicdb.utils.Serverless.span import safe_span


def span(index_of_key: int = 0):
    def add_span(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            args_len = len(args)
            ind = index_of_key
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
def catch_error(error_thrower=None):
    def catch_error_internal(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if error_thrower:
                    error_thrower(e)
                print(f"****REDIS ERROR HERE!**** {f.__name__=}({args=})({kwargs=})", e)
                return None

        return wrapped

    return catch_error_internal


def add_decorators(f, error_thrower=None):
    return catch_error(error_thrower=error_thrower)(span(0)(f))


def decorate_redis(r: redis.Redis, error_thrower=None):
    if getattr(r, "_magic_decorated", False):
        return r

    function_names = [
        "get",
        "mget",
        "set",
        "mset",
        "delete",
        "flushdb",
        "zadd",
        "zscore",
        "zrange",
    ]
    for function_name in function_names:
        if f := getattr(r, function_name, None):
            decorated_f = add_decorators(f=f, error_thrower=error_thrower)
            setattr(r, function_name, decorated_f)

    def pipeline_wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            pipeline = f(*args, **kwargs)
            pipeline.execute = add_decorators(
                pipeline.execute, error_thrower=error_thrower
            )
            return pipeline

        return wrapped

    # add pipeline.execute() as well
    if r.pipeline:
        r.pipeline = pipeline_wrapper(r.pipeline)

    setattr(r, "_magic_decorated", True)
    return r
