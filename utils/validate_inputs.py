
def get_categories(filename):
    categories = [line.rstrip("\n") for line in open(filename)]
    return categories



purchase_categories = get_categories("expense_categories.txt")
