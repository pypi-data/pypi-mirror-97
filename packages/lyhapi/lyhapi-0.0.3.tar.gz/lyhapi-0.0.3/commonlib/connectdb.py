# coding=utf-8
"""
zx08443
"""

import pymysql
from testdata import db


# 数据库连接
def connectdb():
    connect = pymysql.connect(host=db.data["host"], user=db.data["username"], password=db.data["password"],
                              port=db.data["port"], db=db.data["database"])  # 连接数据库
    c = connect.cursor()
    return connect, c  # 返回游标，执行sql语句，返回连接参数，是为了执行数据的更新sql，比如update和delete。
