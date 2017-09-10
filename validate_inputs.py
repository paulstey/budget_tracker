
def get_categories(filename): 
    categories = [line.rstrip("\n") for line in open(filename)]
    return categories


def valid_inputs(vals, categories):
    if vals[1] not in categories:
        print("\nERROR: \'{0}\' is not a defined purchase category.\n".format(vals[1]))
        print("The defined categories include:")
        for c in categories:
            print(c)
        res = False
    else:
        res = True 
    return res 

purchase_categories = get_categories("expense_categories.txt")

