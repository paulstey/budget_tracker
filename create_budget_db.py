#!/usr/env/bin python

import MySQLdb
from utils.password import getpassword



# db = MySQLdb.connect(host = "localhost",
#                      user = "root",
#                      passwd = pswd,
#                      db = "mysql")

def getsql():
    f = open("./create_db.sql", "r")
    sql_code = f.read()
    f.close()
    return sql_code


def main():
    pswd = getpassword()

    # can omit DB specification
    db = MySQLdb.connect(host = "localhost",
                         user = "root",
                         passwd = pswd)

    # cursor object allows query execution
    cur = db.cursor()
    cur.execute("CREATE DATABASE budget;")

    # now connect to `budget` DB
    db2 = MySQLdb.connect(host = "localhost",
                         user = "root",
                         passwd = pswd,
                         db = "budget")
    cur2 = db2.cursor()
    sql_code = getsql()
    cur2.execute(sql_code)


if __name__ == "__main__":
    main()
