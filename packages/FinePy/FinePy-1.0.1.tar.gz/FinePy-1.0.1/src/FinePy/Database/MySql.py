#!/usr/bin/env python
# encoding: utf-8
"""
@File    :   MySql.py
@Author  :   ClanceyHuang 
@Name    :   ...
@Refer   :   unknown
@Desc    :   ...
@Version :   Python3.x
@Contact :   ClanceyHuang@outlook.com
"""

# here put the import lib
import pymysql


class MySql:
    """
    数据库类
    """
    def __init__(self, host, user, passwd, db, port=3306):
        """
        初始化方法
        :param host:
        :param user:
        :param passwd:
        :param db:
        :param port:
        """
        try:
            self.db = pymysql.connect(host=host,
                                      db=db,
                                      user=user,
                                      passwd=passwd,
                                      charset='utf8',
                                      port=port)

            self.cur = self.db.cursor()
            self.dicCur = self.db.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            print(e)
        return

    def commit(self):
        self.db.commit()

    def query(self, sql):
        try:
            a = self.cur.execute(sql)
            return a
        except Exception as e:
            print(e.__str__())
            return False

    def get_one(self, sql):
        self.query(sql)
        self.commit()
        try:
            return self.cur.fetchall()[0]
        except Exception as e:
            print(e)
            return ()

    def get_all(self, sql):
        self.query(sql)
        self.commit()
        try:
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            return []

    def get_dict_one(self, sql):
        try:
            self.dicCur.execute(sql)
            self.commit()
            return self.dicCur.fetchall()[0]
        except Exception as e:
            print(e)
            return None

    def get_dict_all(self, sql):
        try:
            self.dicCur.execute(sql)
            self.commit()
            return self.dicCur.fetchall()
        except Exception as e:
            print(e)
            return []

    def get_last_insert_id(self):
        return self.db.insert_id()

    def close(self):
        try:
            if self.db:
                self.cur.close()  # 关闭指针
                self.db.close()
        except Exception as e:
            print(e)
            pass
