# encoding: utf-8
"""
    @Time   : 2021-03-09 10:30
    @Author : feikong
"""
import time
import types
import threading
from typing import Callable, NoReturn


class Async(object):
    def __init__(self) -> NoReturn: ...

    def __call__(self, f: Callable):
        def fn(*args, **kwargs):
            try:
                threading.Thread(target=f, args=args, kwargs=kwargs).start()
                return
            except Exception as e:
                raise e
        return fn

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return types.MethodType(self, instance)


if __name__ == '__main__':
    @Async()
    def test01():
        for i in range(10):
            print("aaaaaa")
            time.sleep(1)


    @Async()
    def test02():
        for i in range(10):
            print("bbbbbb")
            time.sleep(0.5)


    test01()
    test02()

