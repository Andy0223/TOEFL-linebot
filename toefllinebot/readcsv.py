import pandas as pd
import csv
import chardet

f = pd.read_csv('summary.csv')
print(f.head())
print(f.columns)
print(f['background'])
background = f['background']
for i in background:
    print(i,'\n')
    s='學測'
    j='指考'
    t='多益'
    #if is nan
    if i!=i:
        print(i)
    else:
        sidx = i.find(s)
        jidx = i.find(j)
        tidx = i.find(t)
       
        
    #print(i.split(s))
