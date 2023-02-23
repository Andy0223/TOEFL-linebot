import pandas as pd
import csv
import chardet
import re
f = pd.read_csv('LineBot/summary.csv')
background = f['background']
goal = f['targetScore']
print(goal.head())
sscorelist = []
jscorelist = []
tscorelist = []
goallist = []
def ifelse(condition,yes,value):
    if condition:
        return yes
    else:
        return int(value[0])
    

for idx,i in enumerate(background):
    #print(i,'\n')
    s='學測'
    j='指考'
    t='多益'
    #if is nan
    if i!=i:
        #print(i)
        sscorelist.append(0)
        jscorelist.append(0)
        tscorelist.append(0)
    else:
        i = re.sub(r"\s+", "", i)
        sscore = re.findall(r"(?<=學測)\d\d",i)
        jscore = re.findall(r"(?<=指考)\d\d",i)
        tscore = re.findall(r"(?<=多益)\d\d\d",i)
        

        sscorelist.append(ifelse(len(sscore)==0,0,sscore))
        jscorelist.append(ifelse(len(jscore)==0,0,jscore))
        tscorelist.append(ifelse(len(tscore)==0,0,tscore))
        
    totalscore = re.findall(r"[0-9]+",goal[idx])
    goallist.append(max(map(int,totalscore)))
'''print(sscorelist)
print(len(sscorelist))'''
print(len(f.index))
f['sscore'] = sscorelist
f['tscore'] = tscorelist
f['jscore'] = jscorelist
f['goal'] = goallist
print(type(f))
f['goal'][151] = 97
f['jscore'][151] = 70
f['sscore'][151] = 13
f['tscore'][151] = 850
print(f.iloc[151])
f.to_csv('LineBot/test.csv',index=False)


test = pd.read_csv('LineBot/test.csv')
'''print(test.head())
print(f.columns)'''