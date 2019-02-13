### 数据库API说明

用的是类，默认连接的数据库是本地的ranking数据库，如果要修改的话
在实例化的时候给出位置参数database即可，

如下
```python
    from handle_db.DBApi import DbHandle as DB
    db = DB(database='database_name')
    # 默认情况
    # db = DB(
            # host='localhost', 
            # port=3306, 
            # user='root', 
            # password='131421', 
            # database='ranking'
    #        )
```

现分别对该类的功能说明如下：
```python
# 建表
db.create_table(sql='你写的SQL建表语句')

# 以下三个需要用到表的地方你可以先赋值db.table，这三个函数默认的table是它
# 查询获取数据, _filter默认为None和_range默认为*
db.get(table='你要查询的表名', _filter='过滤器', _range='指定获取的数据的某一列')

# 通过id来查询获取数据, _id可以是个整数（如 1）或者表示id范围的元组（如 (1, 100)，查询的内容是id分别为1到99的数据）
db.get_by_id(table='你要查询的表名', _filter=None ,_id=)

# 保存数据
db.save(table='你要查询的表名', data)

# 执行sql语句
db.execute(query='你要执行的语句')
# 执行多条sql语句
db.executemany(query='你要执行的语句')

# 获取执行语句后的数据
db.fetchone()
db.fetchall()
db.fetchmany(size=)

# 如果有什么用的不方便的地方给我说，我好改

```

