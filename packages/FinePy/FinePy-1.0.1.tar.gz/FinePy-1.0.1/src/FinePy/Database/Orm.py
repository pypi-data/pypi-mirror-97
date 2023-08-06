#!/usr/bin/env python
# encoding: utf-8
"""
@File    :   Orm.py
@Author  :   ClanceyHuang 
@Time    :   2021/02/28 14:10:48
@Name    :   ...
@Refer   :   unknown
@Desc    :   ...
@Version :   Python3.x
@Contact :   ClanceyHuang@gmail.com
"""

# here put the import lib

class Orm:
    def __init__(self, table, db, pkid, factory):
        """
        :param table:
        :param db:
        :param pkid:
        :param OrmFactory factory:
        """
        self.table = table
        self.db = db
        self.pkid = pkid
        self.factory = factory

        # self.cfg = configparser.ConfigParser()
        self.mysql = None
        self.auto_commit = True

        self.debug = False

    # def clear_cache(self, pkid=0):
    #     """
    #     不要频繁调用
    #     :param pkid:
    #     :return:
    #     """
    #     api = config.mysql['cache_api']
    #     request.urlopen(api)

    def get_count_by_where(self, where):
        sql = 'select count(%s) as num from `%s`.`%s` %s' % (
            self.pkid, self.db, self.table, self.make_where(where))
        db = self.get_db()
        one = db.get_dict_one(sql)
        return one['num']

    def get_one_by_wehre(self, where, order='', fields='*'):
        result = self.get_by_where(where, order, '1', fields)
        if len(result) > 0:
            return result[0]
        else:
            return None

    def get_by_where(self, where, order='', limit='', fields='*'):
        sql = 'select %s from `%s`.`%s` %s' % (fields, self.db, self.table,
                                               self.make_where(where))

        if order != '':
            sql += ' order by %s' % (order, )
        if limit != '':
            sql += ' limit %s' % (limit, )
        if self.debug:
            print(sql)

        db = self.get_db()
        data_list = db.get_dict_all(sql)
        return data_list

    def update_by_where(self, where, data):
        sql = "update `%s`.`%s` set %s %s" % (self.db, self.table,
                                              self.make_update_data(data),
                                              self.make_where(where))
        db = self.get_db()
        db.query(sql)
        if self.auto_commit:
            db.commit()
        return True

    def insert_data(self, data):
        sql = "insert `%s`.`%s` set %s" % (self.db, self.table,
                                           self.make_update_data(data))
        db = self.get_db()
        db.query(sql)
        id = db.get_last_insert_id()
        if self.auto_commit:
            db.commit()
        return id

    def update_by_id(self, id, data):
        if 'UNHEX' in str(id):
            sql = "update `%s`.`%s` set %s where `%s`=%s" % (
                self.db, self.table, self.make_update_data(data), self.pkid,
                str(id))
        else:
            sql = "update `%s`.`%s` set %s where `%s`='%s'" % (
                self.db, self.table, self.make_update_data(data), self.pkid,
                str(id))
        db = self.get_db()
        db.query(sql)
        if self.auto_commit:
            db.commit()
        return True

    def delete_by_id(self, id):
        sql = "delete from  `%s`.`%s` where `%s`='%s'" % (self.db, self.table,
                                                          self.pkid, str(id))
        db = self.get_db()
        db.query(sql)
        if self.auto_commit:
            db.commit()
        return True

    def delete_by_where(self, where, data):
        sql = "delete from `%s`.`%s` %s" % (self.db, self.table,
                                            self.make_where(where))
        db = self.get_db()
        db.query(sql)
        if self.auto_commit:
            db.commit()
        return True

    def make_update_data(self, data):
        data_strings = []
        for key, value in data.items():
            value = str(value)
            key = str(key)
            if 'UNHEX' in value:
                data_strings.append("`%s`=%s" % (key, value))
            else:
                data_strings.append("`%s`='%s'" %
                                    (key, pymysql.escape_string(value)))

        return ','.join(data_strings)

    def get_by_id(self, id):
        if 'UNHEX' in str(id):
            sql = "select * from `%s`.`%s` where `%s`=%s" % (
                self.db, self.table, self.pkid, str(id))
        else:
            sql = "select * from `%s`.`%s` where `%s`='%s'" % (
                self.db, self.table, self.pkid, str(id))
        db = self.get_db()
        result = db.get_dict_one(sql)
        return result

    def get_db(self):
        return self.factory.get_db()

    def make_where(self, where):
        fields = []
        for key, value in where.items():
            keys = key.split(' ')
            if len(keys) >= 2:
                field, action = keys
                if action == 'in':
                    if str(type(value)) == "<type 'list'>":
                        value_strings = []
                        for v in value:
                            value_strings.append(str(v))
                        fields.append("`%s` in('%s')" %
                                      (field, "','".join(value_strings)))
                else:
                    value = str(value)
                    fields.append(
                        "`%s` %s '%s'" %
                        (field, action, pymysql.escape_string(value)))
            else:
                fields.append("`%s`='%s'" %
                              (key, pymysql.escape_string(str(value))))
        if len(fields) > 0:
            return 'where ' + ' and '.join(fields)
        else:
            return ''

    def iter_table(self, where, fields='*'):
        limit = '5000'
        order = '%s asc' % (self.pkid, )
        max_id = 0
        while True:
            where['%s >=' % (self.pkid, )] = max_id
            result = self.get_by_where(where=where,
                                       order=order,
                                       limit=limit,
                                       fields=fields)
            for row in result:
                yield row
            max_id = result[len(result) - 1][self.pkid]
            if len(result) < 100:
                break

    def walk_table(self, where, callback):
        limit = '100'
        order = '%s asc' % (self.pkid, )
        max_id = 0
        while True:
            where['%s >=' % (self.pkid, )] = max_id
            result = self.get_by_where(where=where, order=order, limit=limit)
            for row in result:
                callback(row)
            max_id = result[len(result) - 1][self.pkid]
            if len(result) < 100:
                break

    def replace_into(self, data, col, update=False):
        """
        :param data: dic
        :param col: tuple
        :param update: bool
        :return: bool
        """
        where = {col[0]: col[1]}

        if len(self.get_by_where(where)) > 0:
            if update:
                self.update_by_where(where, data)
            return False
        else:
            self.insert_data(data)
            return True
