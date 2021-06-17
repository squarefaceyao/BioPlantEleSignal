# -*- coding = utf-8 -*-
# @Time : 2020/7/22 15:15
# @Author : Zrr
# @File : testSqlite.py
# @Software : PyCharm

import sqlite3

conn = sqlite3.connect("test.db")  #打开或创建数据库文件
print("成功打开数据库")

#建表和插值
c = conn.cursor()  #获取游标

sql = '''
    create table company
    (id int primary key not null,
    name text not null,
    age int not null,
    address char not null,
    salary real);
'''

sqlI = '''
    insert into company(id,name,age,address,salary)
     values(1,'华馨怡',20,'江苏',10000)
'''

c.execute(sql)  #执行sql语句
c.execute(sqlI)
conn.commit()   #提交数据库操作
conn.close()    #关闭数据库连接

print("成功建表")

#查询
# c = conn.cursor()  #获取游标
# sql = "select id,name,salary from company"
# cursor = c.execute(sql)
#
# for row in cursor:
#     print("id= ",row[0])
#     print("name= ", row[1])
#     print("salary= ", row[2],"\n")
#
# conn.close()    #关闭数据库连接
