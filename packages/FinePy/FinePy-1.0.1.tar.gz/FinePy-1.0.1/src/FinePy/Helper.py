#!/usr/bin/env python
# encoding: utf-8
"""
@File    :   Helper.py
@Author  :   ClanceyHuang 
@Name    :   ...
@Refer   :   unknown
@Desc    :   ...
@Version :   Python3.x
@Contact :   ClanceyHuang@outlook.com
"""

# here put the import lib

import os
import re
import socket
import csv
import chardet
import hashlib


def anything2unicode(anything):
    """
    转unicode编码
    :param anything
    """
    coding = chardet.detect(anything)
    return anything.decode(coding['encoding'], 'ignore')


def md5(chars):
    """
    md5方法
    :param chars
    """
    return hashlib.md5(chars).hexdigest()


def get_dir(file_name):
    """
    获取指定文件路径
    :param file_name
    """
    return os.path.dirname(os.path.realpath(__file__)) + '/' + file_name


def del_dir(path):
    """
    清空文件夹下的文件和子目录
    :param path:
    :return:
    """
    for i in os.listdir(path):
        # 取文件绝对路径
        path_file = os.path.join(path, i)
        # 如果是文件，就直接删除，否则就
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_dir(path_file)


def get_tmp_path():
    """
    获取系统临时目录下文件路径
    :return:
    """
    root_path = os.getcwd()
    return root_path + '\\tmp\\'


def get_protocol(address):
    """
    从地址中解析出协议
    :param address:
    :return:
    """
    protocol = address.split("://")[0]
    return protocol


def get_path(address):
    """
    从地址中解析出路径
    :param address:
    :return:
    """
    protocol = get_protocol(address)
    path = address[len(protocol + '://'):]
    path = path.split('?')[0]
    path = path.split(':')[0]
    return path


def get_parameters(address):
    """
    从目标address中分析出携带的参数
    :param address:
    :return:
    """
    param = {}
    key_value_list = address.split("?")[1].split('&')
    for k_y in key_value_list:
        ky = k_y.split('=')
        param[ky[0]] = ky[1]

    return param


def get_port(address):
    """
    从地址中解析出端口
    :param address:
    :return:
    """
    tmp = address.split(':')
    if len(tmp) >= 3:
        port = tmp[-1].strip()
        try:
            port = int(port)
            return port
        except Exception as e:
            print(e)
            return None
    else:
        return None


def is_ip(ip_str):
    """
    检查传入的IP是否正确的IP格式
    :param ip_str:
    :return:
    """
    rex_ip = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if rex_ip.match(ip_str):
        return True
    else:
        return False


def is_port(port):
    """
    检查传入的端口是否是正确的端口范围
    :param port:
    :return:
    """
    if type(port) != int:
        return False

    if 0 <= port <= 65535:
        return True
    else:
        return False


def check_port(ip, port):
    """
    检查端口是否开放
    :param ip
    :param port:
    :return:
    """
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((ip, port))
        sk.close()
        return True
    except Exception as e:
        print(e)
        sk.close()
        return False


def list_to_str(a_list):
    """
    列表转换为字符串
    :param a_list:
    :return:
    """
    return "".join(list(map(str, a_list)))


def str_to_list(t_str):
    """
    字符串转换为列表
    :param t_str:
    :return:
    """
    a_list = []
    for c in str(t_str):
        a_list.append(c)
    return a_list


def read_csv(file_path):
    """
    读取csv文件，返回内容
    :param file_path:
    :return:
    """
    index = 0
    file_content = {}
    csv_file = open(file_path)
    file_reader = csv.reader(csv_file)
    for row in file_reader:
        index += 1
        file_content[index] = row
    csv_file.close()
    return file_content


def dict_res(d, code):
    """
    字典处理
    :param d
    :param code
    """
    result = []
    if isinstance(d, dict) and code in d.keys():
        value = d[code]
        result.append(value)
        return result
    elif isinstance(d, (list, tuple)):
        for item in d:
            value = dict_res(item, code)
            if value == "None" or value is None:
                pass
            elif len(value) == 0:
                pass
            else:
                result.append(value)
        return result
    else:
        if isinstance(d, dict):
            for k in d:
                value = dict_res(d[k], code)
                if value == "None" or value is None:
                    pass
                elif len(value) == 0:
                    pass
                else:
                    for item in value:
                        result.append(item)
            return result
