# -*- coding: utf-8 -*-
"""
:Author: ChenXiaolei
:Date: 2021-02-19 18:19:25
:LastEditTime: 2021-02-23 16:19:58
:LastEditors: ChenXiaolei
:Description: clickhouse帮助类
"""

import clickhouse_driver


class ClickhouseHelper(clickhouse_driver.Client):
    def __init__(self, *args, **kwargs):
        self.clickhouse_client = clickhouse_driver.Client(*args, **kwargs)