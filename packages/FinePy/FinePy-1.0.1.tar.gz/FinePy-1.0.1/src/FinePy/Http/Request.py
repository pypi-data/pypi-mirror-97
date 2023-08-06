#!/usr/bin/env python
# encoding: utf-8
"""
@File    :   Request.py
@Author  :   ClanceyHuang 
@Name    :   ...
@Refer   :   unknown
@Desc    :   ...
@Version :   Python3.x
@Contact :   ClanceyHuang@outlook.com
"""

# here put the import lib

import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class SendRequests:
    """发送请求数据"""
    def __init__(self):
        pass

    def send_requests(self, s, apiData):

        try:
            # 从读取的表格中获取响应的参数作为传递
            method = apiData["method"]
            url = apiData["url"]
            if apiData["params"] == "":
                par = None
            else:
                par = eval(apiData["params"])
            if apiData["headers"] == "":
                h = None
            else:
                h = eval(apiData["headers"])
            if apiData["body"] == "":
                body_data = None
            else:
                body_data = eval(apiData["body"])
            type = apiData["type"]
            v = False
            if type == "data":
                body = body_data
            elif type == "json":
                body = json.dumps(body_data)
            else:
                body = body_data

            # 发送请求
            re = s.request(method=method,
                           url=url,
                           headers=h,
                           params=par,
                           data=body,
                           verify=v)
            return re
        except Exception as e:
            print(e)
