# encoding: utf-8
"""
    @Time   : 2021-03-09 10:36
    @Author : feikong
"""


import unittest


class TestDecorator(unittest.TestCase):

    def test_retry(self):
        from decorator.retry import Retry

        @Retry(tries=3, delay=3)
        def test(*args, **kwargs):
            print("test")
            a = 1 / 0

        with self.assertRaises(ZeroDivisionError):
            test()

    def test_async(self):
        from decorator.async import Async

        print("a")