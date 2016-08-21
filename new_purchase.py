#!/usr/env/bin python

import MySQLdb
import argparse
import datetime
from getpass import getpass


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


def getpassword():
    pw = getpass("Please enter your password: \n")
    return pw 


def getvalues(args):
    vals = []
    vals.append(args.amount)
    vals.append(args.category)
    vals.append(getdate(args))
    vals.append(args.comment)

    if vals[3] == None:
        vals[3] = "NULL"
    return vals 



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
        query = gen_query(vals)
        execute_query(query, pswd)



if __name__ == "__main__":
    main()

