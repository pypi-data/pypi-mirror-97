#!/usr/bin/env python
# encoding: utf-8
"""
@File    :   OrmFactory.py
@Author  :   ClanceyHuang 
@Name    :   ...
@Refer   :   unknown
@Desc    :   ...
@Version :   Python3.x
@Contact :   ClanceyHuang@outlook.com
"""

# here put the import lib


class OrmFactory:
    """一个factory一个connect"""

    def __init__(self, db_config):
        self.db_config = db_config
        self.mysql = None

    def create(self, table, db, pkid='id'):
        return Orm(table, db, pkid, self.db_config)

    def get_table_orm(self, table, pkid='id'):
        return Orm(table, self.db_config['db'], pkid, self)

    def get_db(self):
        try:
            if not self.mysql:
                self.mysql = MySql(self.db_config['host'],
                                   self.db_config['user'],
                                   self.db_config['pass'],
                                   self.db_config['db'])
            else:
                try:
                    self.mysql.db.ping()
                except Exception as e:
                    print(e)
                    self.mysql = MySql(self.db_config['host'],
                                       self.db_config['user'],
                                       self.db_config['pass'],
                                       self.db_config['db'])
        except Exception as e:
            print(e)
            self.mysql = MySql(self.db_config['host'], self.db_config['user'],
                               self.db_config['pass'], self.db_config['db'])
        return self.mysql
