# encoding: utf-8
"""
    @Time   : 2021-03-09 10:31
    @Author : feikong
"""
import time
import types
from typing import NoReturn, Callable


class Retry(object):
    """
    错误重试
    tries 次数
    delay 延迟时间
    用法
    # >>> from decorator.retry import Retry
    # >>> @Retry(tries=3, delay=3)
    # >>> def test():
    #       pass
    # >>> test()
    """

    def __init__(self, tries: int = 3, delay: int = 3) -> NoReturn:
        self.tries = tries
        self.delay = delay

    def __call__(self, f: Callable):
        def fn(*args):
            exception = None
            for _ in range(self.tries):
                try:
                    f(*args)
                    return
                except Exception as e:
                    time.sleep(self.delay)
                    exception = e
            raise exception
        return fn

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return types.MethodType(self, instance)


if __name__ == '__main__':
    @Retry(tries=3, delay=3)
    def test():
        print(time.time())
        a = 1 / 0

    test()
