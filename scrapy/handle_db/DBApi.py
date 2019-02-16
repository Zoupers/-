import pymysql


class DbHandle(object):
    def __init__(self, host='localhost', port=3306, user='root', password='131421', database='ranking', charset='utf8mb4'):
        self.db = pymysql.connect(host=host, port=port, user=user, password=password, charset=charset)
        self.cursor = self.db.cursor()
        self.cursor.execute('SHOW DATABASES')
        if (database,) not in self.cursor.fetchall():
            self.cursor.execute('CREATE DATABASE `%s`' % database)
        self.cursor.execute('USE %s' % database)
        self.table = None

    def create_table(self, sql=None):
        if not sql:
            sql = 'CREATE TABLE `default`(`url` TEXT NOT NULL );'
        self.execute(sql)
        return True

    def delete_table(self, table=None):
        self.execute('DROP TABLE `%s`' % table)

    def get(self, table=None, _filter=None, _range='*'):
        sql = 'SELECT {range} FROM %s'.format(range=_range)
        if not table:
            table = self.table
        select = sql % table
        if _filter:
            self.execute(select+' '+_filter)
        else:
            self.execute(select)
        return self.cursor.fetchall()

    def get_by_id(self, _id, table=None):
        """

        :type table: str table name
        :type _id: int or tuple
        :return:
        """
        assert type(_id) in (int, tuple), '_id 应该是int或者tuple类型，而不是%s' % type(_id)
        if not table:
            table = self.table
        if type(_id) == int:
            _filter = 'WHERE id = {}'.format(_id)
        elif type(_id) == tuple:
            _filter = 'WHERE id >= {} and id < {}'.format(*_id)
        else:
            raise Exception("Unknown Error")
        return self.get(table, _filter=_filter)

    def update(self, data, table=None):
        if not table:
            table = self.table
        sql = 'UPDATE {table} set `{col}`=%s WHERE `id`=%s'.format(table=table)
        sql.format(col=data[0])
        self.execute(sql, data[1:])
        self.db.commit()

    def updatemany(self, data, table=None):
        if not table:
            table = self.table
        for i in data:
            sql = 'UPDATE {table} set `{col}`=%s WHERE `id`=%s'.format(table=table)
            sql.format(col=i[0])
            self.execute(sql, i[1:])
            self.db.commit()

    def save(self, data, table=None, _range=None):
        sql1 = 'INSERT INTO `{table}`'
        sql2 = '{_range} VALUES(%s)'
        if _range:
            sql2 = sql2.format(_range='('+_range+')')
        else:
            sql2 = sql2.format(_range='')
        if not table:
            table = self.table
        sql1 = sql1.format(table=table)
        insert_sql = sql1+sql2
        insert_sql %= ('%s, '*(len(data)-1)+'%s')
        self.execute(insert_sql, data)
        self.db.commit()

    def commit(self):
        self.db.commit()

    def execute(self, query, *args, **kwargs):
        return self.cursor.execute(query, *args, **kwargs)

    def executemany(self, *args, **kwargs):
        return self.cursor.executemany(*args, **kwargs)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchmany(self, size):
        return self.cursor.fetchmany(size)


if __name__ == '__main__':
    db = DbHandle(database='hello')
    print(db.get_by_id(table='students', _id=(1, 5)))

