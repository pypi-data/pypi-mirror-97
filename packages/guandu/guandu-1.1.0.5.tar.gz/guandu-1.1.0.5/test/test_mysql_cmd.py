# encoding: utf-8
"""
    @Time   : 2021-03-08 17:29
    @Author : feikong
"""

import unittest


class TestMysql(unittest.TestCase):

    def test_import(self):
        from db import ExecuteMysql
        func = ExecuteMysql.create_new_report
        # 判断func是否是方法
        self.assertTrue(callable(func))
