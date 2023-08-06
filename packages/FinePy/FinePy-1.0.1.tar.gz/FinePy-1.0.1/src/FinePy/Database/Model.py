#!/usr/bin/env python
# encoding: utf-8
"""
@File    :   Model.py
@Author  :   ClanceyHuang 
@Name    :   ...
@Refer   :   unknown
@Desc    :   ...
@Version :   Python3.x
@Contact :   ClanceyHuang@outlook.com
"""

# here put the import lib
import pymysql


class Model:
    def __init__(self, db_host, db_user, db_passwd, db_name, db_port=3306):
        self.host = db_host
        self.user = db_user
        self.password = db_passwd
        self.database = db_name
        self.port = db_port
        pass

    def query(self, sql):
        db = pymysql.connect(self.host,
                             self.user,
                             self.password,
                             self.database,
                             charset='utf8',
                             self.port)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
        res = cursor.fetchall()
        db.close()
        return res

    def execute(self, sql):
        db = pymysql.connect(self.host,
                             self.user,
                             self.password,
                             self.database,
                             charset='utf8',
                             port=3306)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
            print(e)
        db.close()
