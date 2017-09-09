#!/usr/env/bin python

import MySQLdb
import argparse
import datetime
import os
from getpass import getpass

# my modules
from validate_inputs import valid_inputs 
from validate_inputs import purchase_categories


# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')

# Required positional argument
parser.add_argument('amount', type = float,
                    help = 'Required float positional argument')

# Required positional argument
parser.add_argument('category', type = str, 
                    help = 'Required float positional argument')

# Optional positional argument
parser.add_argument('date_purchased', type = str, nargs = '?',
                    help = 'Optional string positional argument')

# Optional argument
parser.add_argument('--comment', type = str,
                    help='Optional string argument')


# if no date given, this function returns todays
def getdate(args):
    if args.date_purchased == None:
        res = datetime.date.today().strftime("%Y-%m-%d")
    else:
        res = args.date_purchased
    return res 


def print_args(args):
    date = getdate(args)
    print('Amount:   ', args.amount)
    print('Category: ', args.category)
    print('Date:     ', date)
    print('Comment:  ', args.comment)
    print('\n')


def getpassword():
    pw = getpass("Please enter your password: \n")
    return pw 


# returns a list of values in the order below
def getvalues(args):
    vals = []
    vals.append(args.amount)
    vals.append(args.category)
    vals.append(getdate(args))
    vals.append(args.comment)

    if vals[3] == None:
        vals[3] = "NULL"
    return vals 


# returns a string with our insert query
def gen_query(vals):
    query = "INSERT INTO purchases (amount, category, date_purchased, comment) VALUES ({0}, \'{1}\', \'{2}\', {3})".format(vals[0], vals[1], vals[2], vals[3])
    return query 



def execute_query(query, pswd):
    # now connect to `budget` DB
    con = MySQLdb.connect(host = "localhost",    
                         user = "root",        
                         passwd = pswd,  
                         db = "budget")  
    try:
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        print("Successfully inserted new purchase")
    except MySQLdb.IntegrityError:
        print("Failed to insert new purchase")

    return con



def months_totals(con, date):
    first_of_month = date[0:8] + "01"
    query = "SELECT category, sum(amount) FROM (SELECT * FROM purchases WHERE date_purchased >= \'{0}\') tbl1 GROUP BY category;".format(first_of_month)
    
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




def main():
    pswd = getpassword()
    args = parser.parse_args()
    
    print_args(args)
    chk = input("Is the above correct? (y/N)\n")
    
    if chk != "y":
        print("Canceling new purchase insert...")
        return None
    elif chk == "y": 
        vals = getvalues(args)
        if valid_inputs(vals, purchase_categories):
            query = gen_query(vals)
            con = execute_query(query, pswd)
            months_totals(con, vals[2])
            month_to_date_sum(con, vals[2])
        else: 
            print("Canceling new purchase insert...")
    



if __name__ == "__main__":
    os.system("mysql.server start")
    main()
    # os.system("mysql.server stop")

