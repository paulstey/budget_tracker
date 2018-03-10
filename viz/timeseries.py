import pandas as pd
from sqlalchemy import create_engine
import plotnine

# my modules
from utils.password import getpassword


pswd = getpassword()

engine = create_engine('mysql://root:' + pswd + '@localhost/budget')


df_raw = pd.read_sql_table('purchases', engine)

df = df_raw.loc[:, ['amount', 'category', 'date_purchased']]

df_long = df.pivot_table(index = ['date_purchased', 'category'],
                         values = 'amount',
                         aggfunc = 'sum').reset_index()

df_wide = df_long.pivot(index = 'date_purchased',
                        columns = 'category',
                        values = 'amount').reset_index()


grouper = pd.Grouper(key = 'date_purchased', freq = 'M')

grouped_wide_df = df_wide.groupby(grouper)
grouped_long_df = df_long.groupby(grouper)



df_long.index = df_long['date_purchased']
df_long_grp = df_long.groupby(df_long.index.month)
