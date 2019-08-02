import numpy as np
import pandas as pd
import csv
import datetime
import time

result = "Alish_439224627"
#print(type(result.split('_')))
#str = result.split('_')
# = str[1]
#print(str1)
#str1 = (list1[0])

#list1 = ['1', '2', '3']
#str1 = (list1[0])
#print(str1)
print(type(result.split('_')))
str = result.split('_')
name_str = str[0]
id_str = str[1]
id_int = int(id_str)
print(id_int)
print(type(id_int))
print(id_int + 1)
print(name_str)
print(type(name_str))
