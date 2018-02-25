import pandas as pd
from sqlalchemy import create_engine
import plotnine

# my modules
from utils.password import getpassword


pswd = getpassword()

engine = create_engine('mysql://root:' + pswd + '@localhost/budget')


purchases_raw = pd.read_sql_table('purchases', engine)

purchases = purchases_raw.loc[:, ['amount', 'category', 'date_purchased']]

purchases_piv = purchases.pivot_table(index = ['date_purchased', 'category'],
                                      values = 'amount',
                                      aggfunc = 'sum').reset_index()

purchases_wide = purchases_piv.pivot(index = 'date_purchased',
                                     columns = 'category',
                                     values = 'amount').reset_index()


grouper = pd.Grouper(key= 'date_purchased', freq='M')

grouped_df = purchases_wide.groupby(grouper)
