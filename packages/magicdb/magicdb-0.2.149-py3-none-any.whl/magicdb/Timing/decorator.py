import os
from functools import wraps
from time import time
from magicdb.Timing.main import function_times

TIMEIT = os.getenv("TIMEIT")


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        if not TIMEIT:
            return f(*args, **kw)
        start = time()
        result = f(*args, **kw)
        end = time()
        time_took = end - start
        function_times[f.__name__] = function_times.get(f.__name__, 0) + time_took
        print("function_times", function_times)
        return result

    return wrap
