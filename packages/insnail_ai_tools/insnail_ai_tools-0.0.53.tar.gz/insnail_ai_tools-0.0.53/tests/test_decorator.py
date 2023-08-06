import time

import pytest

from insnail_ai_tools.decorator import timeit_decorator


@timeit_decorator
def func1():
    time.sleep(1)
    return 1


@timeit_decorator
async def func2():
    time.sleep(1)
    return 1


def test_timeit_decorator():
    assert func1() == 1


@pytest.mark.asyncio
async def test_timeit_decorator_async():
    result = await func2()
    assert result == 1
