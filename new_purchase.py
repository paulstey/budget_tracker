#!/usr/env/bin python

import MySQLdb
import datetime
import os
import sys
from getpass import getpass

# my modules
from validate_inputs import purchase_categories



class Purchase:
    def __init__(self):
        self.amount = get_value("amount")
        self.category = get_value("category")
        self.date = get_value("date")
        self.comment = get_value("comment")
        self.assemble_vals()


    def assemble_vals(self):
        vals = [self.amount, self.category, self.date, self.comment]
        self.vals = vals


    def is_correct(self):
        print('Amount:   ', self.amount)
        print('Category: ', self.category)
        print('Date:     ', self.date)
        print('Comment:  ', self.comment)
        print('\n')
        print("Is this correct? (y/N)")
        chk = input()
        return chk


    def valid_inputs(self, categories):
        if self.vals[1] not in categories:
            print("\nERROR: \'{0}\' is not a defined purchase category.\n".format(self.vals[1]))
            print("The defined categories include:")
            for c in categories:
                print(c)
            res = False
        else:
            res = True
        return res


    def gen_query(self):
        if self.vals[3] == "":
            self.vals[3] = "NULL"
        query = "INSERT INTO purchases (amount, category, date_purchased, comment) VALUES ({0}, \'{1}\', \'{2}\', \'{3}\')".format(self.vals[0], self.vals[1], self.vals[2], self.vals[3])
        return query


    def insert_purchase(self, con, pswd):
        query = self.gen_query()
        # print(query)

        try:
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            print("Successfully inserted new purchase\n")
        except MySQLdb.IntegrityError:
            print("Failed to insert new purchase")





def get_value(typ):
    if typ == "date":
        print("Enter date (YYYY-MM-DD): ")
        date = input()
        if date == "":
            val = datetime.date.today().strftime("%Y-%m-%d")
        else:
            val = date
    else:
        print("Enter ", typ, ": ", sep = "")
        val = input()
        if val != "":
            val = val
    return val


def getpassword():
    pw = getpass("Please enter your password: \n")
    return pw





def months_totals(con, date):
    first_of_month = date[0:8] + "01"
    query = "SELECT category, sum(amount) AS month_sum FROM (SELECT * FROM purchases WHERE date_purchased >= \'{0}\') tbl1 GROUP BY category ORDER BY month_sum DESC;".format(first_of_month)

    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    print("\nThis month's sub-totals by category:\n")
    for row in rows:
        print(row[0].ljust(16, " "), row[1])
    print("\n")

    con.commit()

def month_to_date_sum(con, date):
    first_of_month = date[0:8] + "01"
    query = "SELECT sum(amount) FROM (SELECT * FROM purchases WHERE date_purchased >= \'{0}\') tbl1;".format(first_of_month)

    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    print("This month's sub-total:\n")
    for row in rows:
        print("  ", row[0], "  ")
    con.commit()


def mysql_running():
    status = os.system("mysql.server status")
    res = status == 0
    return res




def main():
    if len(sys.argv) > 1:
        multi_purchase = sys.argv[1]
    else:
        multi_purchase = None
        
    pswd = getpassword()
    today = datetime.date.today().strftime("%Y-%m-%d")


    # now connect to `budget` DB
    con = MySQLdb.connect(host = "localhost",
                          user = "root",
                          passwd = pswd,
                          db = "budget")

    if (multi_purchase == "-m") or (multi_purchase == "--multiple"):
        another_purchase = True

        while another_purchase:
            purchase = Purchase()
            if purchase.is_correct() == "y" and purchase.valid_inputs(purchase_categories):
                purchase.insert_purchase(con, pswd)
                print("Enter another purchase? (y/N)\n")
                another_purchase = input() == "y"
            else:
                print("Canceling purchase. \n\n")
                print("Would you like to retry? (y/N)\n")
                retry = input()
                if retry != "y":
                    another_purchase = False

    else:
        enter_purchase = True

        while enter_purchase:
            purchase = Purchase()
            if purchase.is_correct() == "y" and purchase.valid_inputs(purchase_categories):
                purchase.insert_purchase(con, pswd)
                enter_purchase = False
            else:
                print("Canceling purchase. \n\n")
                print("Would you like to retry? (y/N)\n")
                retry = input()
                if retry != "y":
                    enter_purchase = False

    months_totals(con, today)
    month_to_date_sum(con, today)



if __name__ == "__main__":

    server_on = mysql_running()
    if not server_on:
        os.system("mysql.server start")

    main()
    # os.system("mysql.server stop")
