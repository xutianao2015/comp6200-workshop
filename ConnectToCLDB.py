#%%
from sqlalchemy import create_engine
import pandas as pd
import pyodbc
import sqlalchemy as sal
#%% create engine
engine = sal.create_engine('mssql+pyodbc://SQLPRD-DSP-01,10433/RPData_DataServices?driver=SQL Server?Trusted_Connection=yes')

# %% create connection
conn = engine.connect()

#%%
print(engine.table_names())
# %%
result = engine.execute('select TOP 100 * from dbo.CSTDAT4787_Output_ForRent_Delta_DT')
# %%
print(result)
# %%
for row in result:
    print (row)
result.close()

# %%
# reading a SQL query using pandas and save as df.
sql_query = pd.read_sql_query('SELECT top 100 * FROM dbo.CSTDAT4787_Output_ForRent_Delta_DT', engine)
# saving SQL table in a pandas data frame
df = pd.DataFrame(sql_query)
# printing the dataframe
df



#%% import into db 
df2 = pd.read_csv('Greater_Bank_Property_Data.csv')
#%% import into db 
# create a new table and append data frame values to this table
df2.to_sql(name = 'GreaterBankInput',schema = 'dbo', con=engine, if_exists='append',index=True,chunksize=1000)

# %% Close connection after all done.
#conn.close()

#%% execute script:
from sqlalchemy import text
#%%
file = open("samplequery.sql",'r')
#print(file.read()) # once read it is going to go to end.
#%%
## it can only execute one query at a time.
#conn.execute(file.read())

#%%
for line in file:
    print(line)
    conn.execute(text(line))
    print(result)

#%%
query = text(file.read())

#%%
conn.execute('SELECT top 10 * FROM dbo.CSTDAT4787_Output_ForRent_Delta_DT;SELECT top 10 * FROM dbo.CSTDAT4787_Output_ForRent_Delta_DT')

#%%
conn.execute(query)

# %%
