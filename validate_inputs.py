#!/usr/env/bin python
purchase_categories = ["rent", "phone", "gym", "internet", "electricity", "utilities", "student loan", "gasoline", "entertainment", "groceries", "supplements", "clothing", "books", "car", "dining out", "alcohol", "travel", "gifts", "misc"]

def valid_inputs(vals, categories):
    if vals[1] not in categories:
        print("ERROR: \'{0}\' is not a defined purchase category.".format(vals[1]))
        res = False
    else:
        res = True 
    return res 
