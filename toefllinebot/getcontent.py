import pandas as pd
import csv
import chardet
import re

st1 = {'background':"900/14/90",'goal':'100','type':'selftaught'}
st2 = {'background':"900/14/90",'goal':'100','type':'cram'}
st3 = {'background':"/15/90",'goal':'100','type':'cram'}
st4 = {'background':"//",'goal':'90','type':'cram'}    
result = st2

def ifelse2(condition,yes,no):
    if condition:
        return yes
    else:
        return no
#print(test.columns)
#print(test['goal'])


#test = pd.read_csv('test.csv')
def getcontent(result):
    
    #print(test.columns)
    #print(test['goal'])


    test = pd.read_csv('test.csv')
    '''if result['background'].split('/')[0]=='' and result['background'].split('/')[1]=='' and result['background'].split('/')[2]=='':
        haveb = 0
    else:
        haveb = 1
        tb = int(result['background'].split('/')[0])
        sb = int(result['background'].split('/')[1])
        jb = int(result['background'].split('/')[2])'''
        
    goal = int(result['goal'])
    artype = ifelse2(result['type']=='cram',1,0)

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
    #if goal+5>120:

    #else goal+5
    ii = 1
    artypeidx2 = artypeidx
    while(len(articleid)<3):
        #print("ii:",ii)
        goalrange = [x for x in range(goal,goal+ii)]
        for i in artypeidx2:
            if test['goal'][i] in goalrange:
                articleid.append(i)
                if len(articleid)==3:
                    break
                artypeidx2.remove(i)
        ii+=1

        if ii==5:
            jj=1
            goalrange1 = [x for x in range(goal-jj,goal)]
            for i in artypeidx2: 
                if test['goal'][i] in goalrange1:
                    articleid.append(i)
                    if len(articleid)==3:
                        break
                    artypeidx2.remove(i)  
            jj+=1
            if jj==3:
                break
    #print(articleid)
    #print("-----------")

    #get reviews:
    for i in articleid:
        ar = [test[j][i] for j in ['rSummary', 'lSummary', 'sSummary', 'wSummary']]
        article.append(ar)
    return len(article)
print(getcontent(st3))

'''

if len(articleid)==3:
    print(articleid)
elif len(articleid)>3:
    #compare background
    print(articleid)
    #how many background:
    #1. sscore
    #2. jscore
    #3. tscore
else:
    #change range to find more review
    #goal+3 if it's still not enough until 120 => goal-3
    print(articleid)'''


'''
#score: score that u want to find
def search(score, colname, idxlist):
    #sameresult: same score in the idxlist
    sameresult = [i for i in idxlist if test[colname][i] == score]     
    if len(sameresult)>=3:
        return sameresult
    else:
    return idxlist
'''