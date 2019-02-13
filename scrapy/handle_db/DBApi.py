import pymysql


class DbHandle(object):
    def __init__(self, host='localhost', port=3306, user='root', password='131421', database='ranking'):
        self.db = pymysql.connect(host=host, port=port, user=user, password=password)
        self.cursor = self.db.cursor()
        self.cursor.execute('SHOW DATABASES')
        if (database,) not in self.cursor.fetchall():
            self.cursor.execute('CREATE DATABASE `%s`' % database)
        self.cursor.execute('USE %s' % database)
        self.table = None

    def create_table(self, sql):
        self.cursor.execute(sql)
        return True

    def get(self, table=None, _filter=None, _range='*'):
        if not table:
            table = self.table
        select = 'SELECT * FROM %s' % table
        if _filter:
            self.cursor.execute(select+' '+_filter)
        else:
            self.cursor.execute(select)
        return self.cursor.fetchall()

    def get_by_id(self, _id, table=None):
        """

        :type table: str table name
        :type _id: int or tuple
        :return:
        """
        assert type(_id) in (int, tuple)
        if not table:
            table = self.table
        if type(_id) == int:
            _filter = 'WHERE id = {}'.format(_id)
        elif type(_id) == tuple:
            _filter = 'WHERE id >= {} and id < {}'.format(*_id)
        else:
            raise Exception("Unknown Error")
        return self.get(table, _filter=_filter)

    def save(self, data, table=None):
        if not table:
            table = self.table
        insert_sql = 'INSERT INTO {table} VALUES {values}'.format(table=table, data=data)
        self.cursor.execute(insert_sql)

    def execute(self, query, *args):
        self.cursor.execute(query, *args)
        return True

    def executemany(self, *args, **kwargs):
        self.cursor.executemany(*args, **kwargs)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchmany(self, size):
        return self.cursor.fetchmany(size)

    def do(self, method, *args, **kwargs):
        pass


if __name__ == '__main__':
    db = DbHandle(database='hello')
    print(db.get_by_id(table='students', _id=(1, 5)))

