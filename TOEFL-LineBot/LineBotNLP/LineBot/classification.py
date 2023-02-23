import jieba
import jieba.analyse
import re
import pandas as pd
from sklearn import preprocessing, naive_bayes
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3
import datetime
import math

def convertToDf(df):
    rClass = ["閱讀"]*len(df)
    df_R = list(df['rContent'])
    lClass = ["聽力"]*len(df)
    df_L = list(df['lContent'])
    sClass = ["口說"]*len(df)
    df_S = list(df['sContent'])
    wClass = ["寫作"]*len(df)
    df_W = list(df['wContent'])

    content = pd.Series(df_R+df_L+df_S+df_W,name='content')
    category = pd.Series(rClass+lClass+sClass+wClass,name='category')
    df1 = pd.concat([content,category],axis=1)

    for i in range(len(df1['content'])):
        if(pd.isna(df1['content'][i]) == True):
            continue
        else:
            df1['content'][i] = re.sub(r"[^/\u4E00-\u9FFF+/ga-zA-Z0-9,，。/\x20/]","",df1['content'][i])

    df1 = df1.dropna(axis=0, how='any')
    return df1

def jiebaProcessing(lst):
    jieba.add_word('閱讀')
    jieba.add_word('聽力')
    jieba.add_word('寫作')
    jieba.add_word('口說')
    seg_list = []
    for item in lst:
        seg = jieba.analyse.extract_tags(item,topK=20)
        # seg = jieba.cut(item)
        seg_list.append(' '.join(seg))
    return seg_list

def msgProcess(msg):
    message = jieba.cut(msg)
    msg_list = []
    msg_list.append(' '.join(message))
    return msg_list

def model(xTrain, xTest, yTrain):
    x_train, x_test, y_train = xTrain, xTest, yTrain
    encoder = preprocessing.LabelEncoder()
    y_train = encoder.fit_transform(y_train)

    # #建立一個向量計數器物件
    count_vect = CountVectorizer(analyzer='word')
    count_vect.fit(x_train)

    #使用向量計數器物件轉換訓練集和驗證集
    x_train = count_vect.transform(x_train)
    x_test = count_vect.transform(x_test)

    mb = naive_bayes.MultinomialNB()
    # fit the training dataset on the classifier
    mb.fit(x_train, y_train)
    # predict the labels on validation dataset
    predict = mb.predict(x_test)
    predict = encoder.inverse_transform(predict)[0]
    print(predict)
    return predict

def dbInsert(msg,predict,uid):
    try:
        tzone = datetime.timezone(datetime.timedelta(hours=8))
        con = sqlite3.connect("final.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS final(uid, content, myDate DATETIME, type)")
        cur.execute(f"""
            INSERT INTO final VALUES
                ('{uid}','{msg}','{datetime.datetime.now(tz=tzone).strftime("%Y-%m-%d %H:%M:%S")}', '{predict}')
            """)
        con.commit()
        print("done")
        return f"新增{predict}成功"
    except:
        return "新增失敗"
    finally:
        con.close()
def dbInsertUser(uid,uname):
    try:
        con = sqlite3.connect("final.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS user(uid, uname)")
        cur.execute(f"""
            INSERT OR IGNORE INTO user VALUES
                ('{uid}','{uname}')
            """)
        con.commit()
        print("done")
        return f"新增{uname}至資料庫中"
    except:
        return "新增失敗"
    finally:
        con.close()

def dbQuery(category,uid):
    try:
        con = sqlite3.connect("final.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT * FROM final WHERE type='{category}' AND uid='{uid}' ORDER BY myDate desc")
        data = res.fetchall()
        print('hi')
        print(data)
        cont = []
        dt = []
        if(len(data) == 0):
            cont = "無法查詢，請重新輸入"
            dt = "無法查詢，請重新輸入"
        else:
            for i in range(len(data)):
                cont.append(data[i][1])
                dt.append(data[i][2])
        # temp = '/'.join(temp)
        return cont,dt
    except:
        return "無法查詢，請重新輸入"
    finally:
        con.close()

def dbQueryPercentage(uid):
    try:
        con = sqlite3.connect("final.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT * FROM final WHERE uid='{uid}'")
        data = res.fetchall()
        print(data)
        cntR = 0
        cntL = 0
        cntS = 0
        cntW = 0
        if(len(data) == 0):
            return "你尚未建立任何學習歷程，請輸入『新增日記』"
        else:
            for i in range(len(data)):
                if(data[i][3] == "閱讀"):
                    cntR +=1
                elif(data[i][3] == "聽力"):
                    cntL +=1
                elif(data[i][3] == "口說"):
                    cntS +=1
                elif(data[i][3] == "寫作"):
                    cntW +=1
                else:
                    pass
        # print(round(cntR/len(data),1),cntL/len(data),cntS/len(data),cntW/len(data))
        percentage = {"閱讀":cntR,"聽力":cntL,"口說":cntS,"寫作":cntW}
        total = cntR+cntL+cntS+cntW
        print(percentage)
        print(total)
        return percentage,total
    except:
        return "無法查詢，請重新輸入"
    finally:
        con.close()

def Insert(msg,uid):
    dataframe = pd.read_csv('/Users/andy/Downloads/summary.csv') 
    content = convertToDf(dataframe)
    contentTag = jiebaProcessing(list(content['content']))
    userInput = msgProcess(msg)
    category = list(content['category'])
    prediction = model(contentTag,userInput,category)
    alert = dbInsert(msg,prediction,uid)
    return alert

def Query(msg):
    return dbQuery(msg)


# if __name__ == "__main__":
#     print(dbQuery('聽力'))
    # dataframe = pd.read_csv('/Users/andy/Downloads/summary.csv') 
    # content = convertToDf(dataframe)
    # contentTag = jiebaProcessing(list(content['content']))
    # userInput = msgProcess(input())
    # category = list(content['category'])
    # prediction = model(contentTag,userInput,category)
    # print(prediction)
    












