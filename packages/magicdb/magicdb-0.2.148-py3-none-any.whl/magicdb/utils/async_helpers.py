import concurrent.futures

import asyncio
from functools import wraps

_DEFAULT_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=20)
# _DEFAULT_POOL._max_workers = max(_DEFAULT_POOL._max_workers, 20)


def magic_async(f, executor=None):
    """Makes a sync function async by returning asyncio futures that can be awaited.
    Function takes in a sync param and if False, will return an awaitable promise"""

    @wraps(f)
    def wrap(*args, sync=True, future=False, **kwargs):
        if sync and not future:
            return f(*args, **kwargs)
        future_res = (executor or _DEFAULT_POOL).submit(f, *args, **kwargs)
        if future:
            return future_res
        return asyncio.wrap_future(future_res)

    return wrap


def get_futures(futures):
    return [future.result() for future in futures]


def threadpool_asyncio(f, executor=None):
    """Makes a sync function async by returning asyncio futures that can be awaited."""

    @wraps(f)
    def wrap(*args, **kwargs):
        future = (executor or _DEFAULT_POOL).submit(f, *args, **kwargs)
        return asyncio.wrap_future(future)

    return wrap


def threadpool(f, executor=None):
    @wraps(f)
    def wrap(*args, **kwargs):
        future = (executor or _DEFAULT_POOL).submit(f, *args, **kwargs)
        return future

    return wrap


def promise(f, executor=None):
    """Makes async function a task -- to be executed concurrently."""

    @wraps(f)
    def wrap(*args, **kwargs):
        return asyncio.create_task(f(*args, **kwargs))

    return wrap
