# -*- coding: utf-8 -*-
from typing import Optional
import sqlite3


class SqliteDB:

    def __init__(self, database="default.db") -> None:
        try:
            self.conn = sqlite3.connect(database)
            self.cursor = self.conn.cursor()    # 创建一个cursor
        except Exception as e:
            print(e)

    def execute(self, sql: Optional[str]) -> int:
        """
        返回执行execute()方法后影响的行数
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        rowcount = self.cursor.rowcount
        return rowcount

    def delete(self, table_name: Optional[str], **kwargs) -> int:
        """
        删除并返回影响行数
        :param table_name:
        :param kwargs:
        :return:
        """
        where_str = f"where {kwargs['where']}" if kwargs.get('where', '') else ''
        sql = f"delete from {table_name} {where_str}"
        print(sql)
        try:
            self.cursor.execute(sql)    # 执行SQL语句
            self.conn.commit()  # 提交到数据库执行
        except Exception as e:
            print(f"tables delete  error: {e}")
            self.conn.rollback()    # 发生错误时回滚
        return self.cursor.rowcount

    def insert(self, table_name: Optional[str], **kwargs) -> int:
        """
        新增并返回新增ID
        :param table_name:
        :param kwargs:
        :return:
        """
        fields_list = []
        values_list = []
        symbol_list = []
        for k, v in kwargs.items():
            fields_list.append(str(k))
            values_list.append(str(v))
            symbol_list.append('?')
        sql = f"insert into {table_name} ({','.join(fields_list)}) values ({','.join(symbol_list)})"
        print(sql)
        res = 0
        try:
            self.cursor.execute(sql, tuple(values_list))  # 执行SQL语句
            self.conn.commit()  # 提交到数据库执行
            res = self.cursor.lastrowid  # 获取自增id
        except Exception as e:
            print(f"tables insert  error: {e}")
            self.conn.rollback()  # 发生错误时回滚
        return res

    def update(self, table_name: Optional[str], where: Optional[str], **kwargs) -> int:
        """
        修改数据并返回影响的行数
        :param table_name:
        :param where:
        :param kwargs:
        :return:
        """
        update_list = []
        values_list = []
        for k, v in kwargs.items():
            update_list.append(f"{k}=?")
            values_list.append(v)
        sql = f'update {table_name} set {",".join(update_list)} where {where}'
        print(sql)
        rowcount = 0
        try:
            self.cursor.execute(sql, tuple(values_list))  # 执行SQL语句
            self.conn.commit()  # 提交到数据库执行
            rowcount = self.cursor.rowcount  # 影响的行数
        except Exception as e:
            print(f"tables update error: {e}")
            self.conn.rollback()  # 发生错误时回滚
        return rowcount

    def get_first(self, table_name: Optional[str], **kwargs) -> list:
        """
        查询一条数据
        :param table_name:
        :param kwargs:
        :return:
        """
        field = ','.join(kwargs['field']) if kwargs.get('field', '') else '*'
        where = f"where {kwargs['where']}" if kwargs.get('where', '') else ''
        order = f"order by {kwargs['order']}" if kwargs.get('order', '') else ''
        sql = f'select {field} from {table_name} {where} {order}'
        print(sql)
        data = []
        try:
            self.cursor.execute(sql)        # 执行SQL语句
            data = self.cursor.fetchone()   # 使用fetchone方法获取单条数据.
        except Exception as e:
            print(f"tables select error: {e}")
            self.conn.rollback()    # 发生错误时回滚
        return data

    def get_all(self, table_name: Optional[str], **kwargs) -> list:
        """
        查所有数据
        :param table_name:
        :param kwargs:
        :return:
        """
        field = ','.join(kwargs['field']) if kwargs.get('field', '') else '*'
        where = f"where {kwargs['where']}" if kwargs.get('where', '') else ''
        order = f"order by {kwargs['order']}" if kwargs.get('order', '') else ''
        sql = f'select {field} from {table_name} {where} {order}'
        print(sql)
        data = []
        try:
            self.cursor.execute(sql)    # 执行SQL语句
            query_data = self.cursor.fetchall()
            for item in query_data:
                data.append({k: v for k, v in zip(kwargs['field'], item)})
        except Exception as e:
            print(f"tables select error: {e}")
            self.conn.rollback()    # 发生错误时回滚
        return data

    def create_table(self, sql: Optional[str] = None, table_name: Optional[str] = None, drop: Optional[bool] = False) -> bool:
        """
        创建表
        :param sql:
        :param table_name:
        :param drop:
        :return:
        """
        if table_name is None:
            print("table参数不能为空")
            return False

        # 强制清空
        if drop:
            self.drop_table(table_name)

        # 查看表格是否已经存在
        self.cursor.execute(f"SELECT COUNT(*) FROM sqlite_master where type='table' and name='{table_name}'")
        values = self.cursor.fetchall()
        existtb = values[0][0]

        if existtb == 0:
            # 执行一条SQL语句：创建user表 'CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name VARCHAR)'
            self.cursor.execute(sql)
            # return self.cursor.rowcount
            return True
        return False

    def drop_table(self, table_name: Optional[str] = None) -> bool:
        if table_name is None:
            print("表名不能为空")
            return False
        self.cursor.execute(f"drop table if exists {table_name}")
        # return self.cursor.rowcount
        return True

    def __del__(self):
        self.conn.close()  # 关闭连接


if __name__ == '__main__':
    db = SqliteDB()
    # sql = "CREATE TABLE asin (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, asin VARCHAR, status VARCHAR, title VARCHAR, cover VARCHAR, stars double, lreviewdate VARCHAR, description VARCHAR, url VARCHAR, atime timestamp NULL DEFAULT NULL, mtime timestamp NULL DEFAULT NULL, price double, flag INTEGER DEFAULT 0, reviewcount INTEGER DEFAULT 0)"
    # res = db.create_table(sql=sql, table_name='asin')
    # print(res)

    # asin = ''
    # for i in range(5):
    #     asin += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    #
    # # insert测试
    # cs = db.insert(table_name="asin", asin=asin, title="标题" + str(random.randint(100, 999)), stars=4.3)
    # print(cs)

    # # delete 测试
    # cs = db.delete(table="asin", where="id=6")
    # print(cs)

    # update 测试
    cs = db.update(table_name="asin", where="id=1", title="8888", stars=4.9, status='正常')
    print(cs)

    # select 测试
    # cs = db.get_all(table_name="asin", where="id=1")
    # print(cs)

