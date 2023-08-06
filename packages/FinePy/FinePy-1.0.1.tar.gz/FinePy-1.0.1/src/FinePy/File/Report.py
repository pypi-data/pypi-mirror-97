#!/usr/bin/env python
# encoding: utf-8
"""
@File    :   Report.py
@Author  :   ClanceyHuang 
@Name    :   ...
@Refer   :   unknown
@Desc    :   ...
@Version :   Python3.x
@Contact :   ClanceyHuang@outlook.com
"""

# here put the import lib

import os


def WriteReport(test_report):
    """
    生成最新的测试报告文件
    :param test_report:
    :return:返回文件
    """
    lists = os.listdir(test_report)
    lists.sort(key=lambda fn: os.path.getmtime(test_report + "/" + fn))
    file_new = os.path.join(test_report, lists[-1])
    return file_new
