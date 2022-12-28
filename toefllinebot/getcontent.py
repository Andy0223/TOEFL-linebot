import pandas as pd
import csv
import chardet
import re

st1 = {'background':"900/14/90",'goal':'100','type':'selftaught'}
st2 = {'background':"900/14/90",'goal':'100','type':'cram'}
st3 = {'background':"/15/90",'goal':'100','type':'cram'}
st4 = {'background':"//",'goal':'90','type':'cram'}    
test = pd.read_csv('test.csv')

def ifelse(condition,yes,no):
    if condition:
        return yes
    else:
        return no
print(test.columns)

print(test['goal'])

result = st1

if result['background'].split('/')[0]=='' and result['background'].split('/')[1]=='' and result['background'].split('/')[2]=='':
    haveb = 0
else:
    haveb = 1
    tb = int(result['background'].split('/')[0])
    sb = int(result['background'].split('/')[1])
    jb = int(result['background'].split('/')[2])
    
goal = int(result['goal'])
artype = ifelse(result['type']=='cram',1,0)

#type => 
#1. find totally same goal
#if enough: stop
#elif not enough: find+1
#elif not enough: 
#print(test.index[test['tutoring'] == artype].tolist())
artypeidx = test.index[test['tutoring'] == artype].tolist()

#符合條件的id先存到articleid裡
articleid = []
article = []
'''while(len(article)<3):'''



#index of reviews' goal == user's goal
#[i for i in artypeidx if test['goal'][i]==goal]
[articleid.append(i) for i in artypeidx if test['goal'][i]==goal]
print(articleid)

if len(articleid)==3:
    print(articleid)
elif len(articleid)>3:
    #compare background
    print(articleid)
else:
    #change range to find more review
    #goal+3 if it's still not enough until 120 => goal-3
    print(articleid)


