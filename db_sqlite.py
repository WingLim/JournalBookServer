import sqlite3

class DBSqlite():

    def __init__(self):
        self.dbname = 'data/journal.db'
    
    # 连接到数据库
    def connect(self):
        conn = sqlite3.connect(self.dbname)
        cu = conn.cursor()
        return conn, cu
    
    # 关闭连接
    def disconnect(self, conn, cu):
        cu.close()
        conn.close()
    
    # 创建表
    def create_table(self, table):
        conn, cu = self.connect()
        cu.execute('''CREATE TABLE '{}'
        (   KEY TEXT PRIMARY KEY NOT NULL,
            VAL TEXT
        );'''.format(table))
        conn.commit()
        self.disconnect(conn, cu)
    
    # 删除表
    def drop_table(self, table):
        conn, cu = self.connect()
        sql = 'DROP TABLE IF EXISTS ' + table
        cu.execute(sql)
        conn.commit()
        self.disconnect(conn, cu)
    
    # 插入一条数据
    def insert(self, table, key, val):
        conn, cu = self.connect()
        sql = '''INSERT INTO '{}' VALUES (
            '{}',
            '{}'
        );'''.format(table, key, val)
        try:
            with conn:
                cu.execute(sql)
        except sqlite3.IntegrityError:
            sql = '''UPDATE {}
            SET VAL = '{}' WHERE KEY = '{}'
            '''.format(table, val, key)
            with conn:
                cu.execute(sql)
        self.disconnect(conn, cu)
    
    # 获取数据
    def fetch(self, table, key):
        conn, cu = self.connect()
        sql = "SELECT * FROM '{}' WHERE KEY = '{}';".format(table, key)
        cu.execute(sql)
        r = cu.fetchall()
        self.disconnect(conn, cu)
        return r
    
    # 获取所有 key
    def fetchkeys(self, table):
        conn, cu = self.connect()
        sql = "SELECT KEY FROM '{}'".format(table)
        cu.execute(sql)
        r = cu.fetchall()
        self.disconnect(conn, cu)
        return r

    # 删除数据
    def delete(self, table, key):
        conn, cu = self.connect()
        sql = "DELETE FROM '{}' WHERE KEY = '{};".format(table, key)
        cu.execute(sql)
        conn.commit()
        r = cu.fetchall()
        self.disconnect()
        return r