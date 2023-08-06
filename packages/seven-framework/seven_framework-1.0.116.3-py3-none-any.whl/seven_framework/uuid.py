# -*- coding: utf-8 -*-
"""
:Author: ChenXiaolei
:Date: 2020-04-16 14:38:22
:LastEditTime: 2020-04-22 15:13:52
:LastEditors: ChenXiaolei
:Description: uuid helper
"""
import uuid


class UUIDHelper:
    @classmethod
    def get_uuid(self):
        """
        :Description: 获取uuid4
        :return: uuid字符串
        :last_editors: ChenXiaolei
        """
        return str(uuid.uuid4())