import pandas as pd
import numpy as np
import csv
import time
from datetime import datetime
now = datetime.now()
time = now.strftime("%A:%H:%M")
print(time)
"""
df_data = pd.read_csv('schooldata.csv')
#print(df_data.shape)
#print(df_data.head())
age = "439224627"
#439224627

print(type(age))
ageint = int(age)
print(type(ageint))

df_data = df_data[df_data["parent_id"] == ageint]
if (df_data["parent_id"] == ageint).all():
    print(df_data.iloc[0])
    print(df_data['child_name'].iloc[0])
if (df_data.empty):
    print("NO")

#df_data = df_data[df_data["parent_id"] == 5]
#print(df_data)



#print(df_data.loc[:  , ['status']])
#if(df_data.loc[: , ['status']] == "False").all():
#    print("NONE")
#else:
#    print(df_data.head())
#if (df_data["parent_id"] == 5).all():
#    print(df_data)
#else:
#    print("NO")


"""
