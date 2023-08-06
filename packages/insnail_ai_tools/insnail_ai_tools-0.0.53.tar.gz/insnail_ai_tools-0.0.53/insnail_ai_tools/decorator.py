import functools
import inspect
import time


def timeit_decorator(func):
    def _echo_time(func_, t0, t1):
        total_time = t1 - t0
        print(f"func [{func_.__name__}], [{total_time}] seconds")

    @functools.wraps(func)
    def wrap(*args, **kwargs):
        _t0 = time.time()
        _r = func(*args, **kwargs)
        _t1 = time.time()
        _echo_time(func, _t0, _t1)
        return _r

    @functools.wraps(func)
    async def wrap_async(*args, **kwargs):
        _t0 = time.time()
        _r = await func(*args, **kwargs)
        _t1 = time.time()
        _echo_time(func, _t0, _t1)
        return _r

    if inspect.iscoroutinefunction(func):
        return wrap_async
    else:
        return wrap
