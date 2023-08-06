#!/usr/bin/env python
# encoding: utf-8
"""
@File    :   Assert.py
@Author  :   ClanceyHuang 
@Name    :   ...
@Refer   :   unknown
@Desc    :   ...
@Version :   Python3.x
@Contact :   ClanceyHuang@outlook.com
"""

# here put the import lib

from Helper import dict_res
from Log import LOG, logger


@logger('断言测试结果')
def assert_in(assert_wish, final_result):
    if len(assert_wish.split('=')) > 1:
        data = assert_wish.split('&')
        result = dict([(item.split('=')) for item in data])
        value1 = ([(str(dict_res(final_result, key)))
                   for key in result.keys()])
        value2 = ([(str(value)) for value in result.values()])
        if value1 == value2:
            return {'code': 0, "result": 'pass'}
        else:
            return {'code': 1, 'result': 'fail'}
    else:
        LOG.info('填写测试预期值')
        return {"code": 2, 'result': '填写测试预期值'}


@logger('断言测试结果')
def assert_re(assert_wish):
    if len(assert_wish.split('=')) > 1:
        data = assert_wish.split('&')
        result = dict([(item.split('=')) for item in data])
        return result
    else:
        LOG.info('填写测试预期值')
        return {"code": 1, 'result': '填写测试预期值'}
