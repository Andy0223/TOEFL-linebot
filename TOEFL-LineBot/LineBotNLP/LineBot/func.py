
from django.conf import settings
import pandas as pd
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    PostbackEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    ConfirmTemplate,
    MessageTemplateAction,
    PostbackTemplateAction,
    FlexSendMessage
)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

def storevalue(type,value,result):
    if type=="background":
        result['background'] = value
    elif type=="goal":
        result['goal'] = value
    elif type=="type":
        result['type'] = value
    print("result:",result)

def backgroundbutton(event):
    try:
        Confirm_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ConfirmTemplate(
            title='是否提供您的背景',
            text='是否提供您的背景?\n我們可以搜尋到跟您背景類似的心得文',
            actions=[                              
                PostbackTemplateAction(
                    label='Yes',
                    text='Yes',
                    data='action=backgroundyes'
                ),
                PostbackTemplateAction(
                    label='Skip',
                    text='Skip',
                    data='A&' + '//'
                ),
            ]
        )
        )
        line_bot_api.reply_message(event.reply_token,Confirm_template)
        
        '''backgroundinfo = "請輸入您的背景(多益/學測/指考):\n範例一: 800/14/82\n範例二: 700//10\n請按照格式輸入，無分數可不用輸入，如範例二"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=backgroundinfo))'''
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
def backgroundmessage(event):
    try:
        flex_message = FlexSendMessage(
        alt_text = 'flex',
        contents=
            {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "請輸入您的背景(多益/學測/指考):",
                        "weight": "bold",
                        "size": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "範例一",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "mybackground\n800/14/82",
                                "wrap": True,
                                "color": "#666666",
                                "size": "sm",
                                "flex": 5
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "範例二",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "mybackground\n700//10",
                                "wrap": True,
                                "color": "#666666",
                                "size": "sm",
                                "flex": 5
                            }
                            ]
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "mybackground後要下一行，分數之間用/隔開，無分數可不用輸入，如範例二",
                                    "wrap": True,
                                    "size": "sm",
                                    "flex": 1
                                },
                                ]
                            }
                        ]
                        
                    },
                    ]
                }
            }
        
        ),
        line_bot_api.reply_message(event.reply_token, flex_message)
    
    
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
#background score in wrong range
def backgroundmessage_rangewrong(event):
    try:
        flex_message = FlexSendMessage(
        alt_text = 'flex',
        contents=
            {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "範圍錯誤，請再輸入一次",
                            "wrap": True,
                            "size": "sm",
                            "flex": 1
                        },
                        ]
                    },


                    {
                        "type": "text",
                        "text": "請輸入您的背景(多益/學測/指考):",
                        "weight": "bold",
                        "size": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "範例一",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "mybackground\n800/14/82",
                                "wrap": True,
                                "color": "#666666",
                                "size": "sm",
                                "flex": 5
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "範例二",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "mybackground\n700//10",
                                "wrap": True,
                                "color": "#666666",
                                "size": "sm",
                                "flex": 5
                            }
                            ]
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "mybackground後要下一行，分數之間用/隔開，無分數可不用輸入，如範例二",
                                    "wrap": True,
                                    "size": "sm",
                                    "flex": 1
                                },
                                ]
                            }
                        ]
                        
                    },
                    ]
                }
            }
        
        ),
        line_bot_api.reply_message(event.reply_token, flex_message)
    
    
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))


def backgroundconfirmbutton(event):
    try:
        score = event.message.text.split('\n')[1].split('/')
        #print(event.message.text)
        backgroundconfirmtext = '您的英文背景如下:\n'+"多益:"+score[0]+"分\n學測:"+score[1]+"級\n指考:"+score[2]+"分\n"+"是否正確:"
        Confirm_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ConfirmTemplate(
            title='是否提供您的背景',
            text=backgroundconfirmtext,
            actions=[                              
                PostbackTemplateAction(
                    label='正確',
                    text='正確',
                    data='A&' + event.message.text.split('\n')[1]
                ),
                PostbackTemplateAction(
                    label='錯誤',
                    text='錯誤',
                    data='action=backgroundfalse'
                ),
            ]
        )
        )
        line_bot_api.reply_message(event.reply_token,Confirm_template)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
def goalmessage(event):
    try:
        flex_message = FlexSendMessage(
        alt_text = 'flex',
        contents=
            {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "請問你的目標總分為何?(必填)",
                        "weight": "bold",
                        "size": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "(70~120分)"
                        }
                        ],
                        "position": "relative"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "範例一",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "mygoal\n100",
                                "wrap": True,
                                "color": "#666666",
                                "size": "sm",
                                "flex": 5
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "範例二",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "mygoal\n85",
                                "wrap": True,
                                "color": "#666666",
                                "size": "sm",
                                "flex": 5
                            }
                            ]
                        }
                        ]
                    }
                    ]
                }
            }
        
        ),
        line_bot_api.reply_message(event.reply_token, flex_message)
    
    
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def goalconfirmbutton(event):
    try:
        score1 = event.message.text.split('\n')[1]
        goalconfirmtext = '所以您的目標總分是:\n'+score1+"\n"+"是否正確:"
        Confirm_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ConfirmTemplate(
            title='goal',
            text=goalconfirmtext,
            actions=[                              
                PostbackTemplateAction(
                    label='正確',
                    text='正確',
                    data='B&' + score1
                ),
                PostbackTemplateAction(
                    label='錯誤',
                    text='錯誤',
                    data='action=goalfalse'
                ),
            ]
        )
        )
        line_bot_api.reply_message(event.reply_token,Confirm_template)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
#article type
def typebutton(event):
    try:
        message = TemplateSendMessage(
            alt_text = '按鈕樣板',
            template = ButtonsTemplate(
                #thumbnail_image_url='https://i.imgur.com/pRdaAmS.jpg',
                title='article type',
                text='請問您想看甚麼類型的文章',
                actions=[
                    PostbackTemplateAction(
                        label='自學文',
                        text='自學文',
                        data='C&selftaught'
                    ),
                    PostbackTemplateAction(
                        label='補習文',
                        text='補習文',
                        data='C&cram'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

#subjectbutton

#get content from csv file function

def ifelse2(condition,yes,no):
    if condition:
        return yes
    else:
        return no
test = pd.read_csv('LineBot/test.csv')
def getcontent(result):
    
    print(test.columns)
    #print(test['goal'])


    
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
    artypeidx2 = artypeidx
    #if goal+5>120:
    if goal+5>120:
        ii = 1
        while(len(articleid)<3):
          goalrange = [x for x in range(goal,goal+ii)]
          for i in artypeidx2:
            if test['goal'][i] in goalrange:
                articleid.append(i)
                if len(articleid)==3:
                    break
                artypeidx2.remove(i)
          ii+=1
          if goal+ii==121:
              break
        jj=1
        while(len(articleid)<3):
          goalrange1 = [x for x in range(goal-jj,goal)]
          for i in artypeidx2:
              if test['goal'][i] in goalrange1:
                  articleid.append(i)
                  if len(articleid)==3:
                      break
                  artypeidx2.remove(i)
              jj+=1     
    elif goal-3<80:
      ii = 1
      while(len(articleid)<3):
          goalrange = [x for x in range(goal,goal+ii)]
          for i in artypeidx2:
              if test['goal'][i] in goalrange:
                    articleid.append(i)
                    if len(articleid)==3:
                        break
                    artypeidx2.remove(i)
          ii+=1    
    else:
        
        a = 1
        jj=1
        while(len(articleid)<3):
          #print("ii:",ii)
          if a==5:
              
              
              goalrange1 = [x for x in range(goal-jj,goal)]
              print(goalrange1)
              
              for i in artypeidx2: 
                  if test['goal'][i] in goalrange1:
                      articleid.append(i)
                      print(articleid)
                      if len(articleid)==3:
                          break
                      artypeidx2.remove(i)  
              jj+=1
              if jj==3:
                  print("werwer")
                  break
          else:

            goalrange = [x for x in range(goal,goal+a)]
            print(goalrange)
            for i in artypeidx2:
                if test['goal'][i] in goalrange:
                    articleid.append(i)
                    if len(articleid)==3:
                          break
                    artypeidx2.remove(i)
            a+=1  
          
          
        
        if len(articleid)<3:
          kk = a
          while(len(articleid)<3):
              if goal+kk == 121:
                  break
              goalrange3 = [x for x in range(goal, goal+kk)]
              for i in artypeidx2: 
                  if test['goal'][i] in goalrange3:
                      articleid.append(i)
                      if len(articleid)==3:
                          break
                      artypeidx2.remove(i)
              kk+=1
        
        if len(articleid)<3:
          ll = jj
          while(len(articleid)<3):
              goalrange3 = [x for x in range(goal-ll, goal)]
              for i in artypeidx2: 
                  if test['goal'][i] in goalrange3:
                      articleid.append(i)
                      if len(articleid)==3:
                          break
                      artypeidx2.remove(i)
              ll+=1
        


    #print(articleid)
    #print("-----------")
    
    #get reviews:
    #get total toefl score:
    totalscore = []
    for i in articleid:
        ar = [str(test[j][i]) for j in ['rSummary', 'lSummary', 'sSummary', 'wSummary','goal']]
        article.append(ar)
    return article
#print(len(getcontent({'background':"900/14/90",'goal':'100','type':'cram'})))


#subjectmessage
def subjectmessage(event,result):
    #getcontent(result) -> 
    #1: ['reading','listening','speaking','writing]
    #2: ...
    #[ [#1], [#2], [#3] ]
    article = getcontent(result)
    #print(type(article[0][4]))
    #article = [ ['11','22','33','44'], ['11','22','33','44'],['11','22','33','44']]
    #print(result)
    try:
        flex_message = FlexSendMessage(
        alt_text = 'flex',
        contents=
            {
              "type": "carousel",
              "contents": [
                {
                  "type": "bubble",
                  "size": "mega",
                  "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "Reading",
                        "weight": "bold",
                        "size": "sm",
                        "wrap": True
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                              {
                                "type": "text",
                                "text": "1. ",
                                "margin": "none",
                                "size": "xs",
                                "flex": 0
                              },
                              {
                                "type": "text",
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5,
                                "text": article[0][0] + '\n\n' + 'TOTAL: '+ article[0][4]
                              }
                            ],
                            "paddingAll": "10px"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                              {
                                "type": "text",
                                "text": "2. ",
                                "margin": "none",
                                "size": "xs",
                                "flex": 0
                              },
                              {
                                "type": "text",
                                "text": article[1][0] + '\n\n' + 'TOTAL: '+ article[1][4],
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                              }
                            ],
                            "paddingAll": "10px"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                              {
                                "type": "text",
                                "text": "3. ",
                                "margin": "none",
                                "size": "xs",
                                "flex": 0
                              },
                              {
                                "type": "text",
                                "text": article[2][0] + '\n\n' + 'TOTAL: '+ article[2][4],
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                              }
                            ],
                            "flex": 5,
                            "paddingAll": "10px"
                          }
                        ]
                      }
                    ],
                    "spacing": "sm",
                    "paddingAll": "10px"
                  }
                },
                {
                  "type": "bubble",
                  "size": "mega",
                  "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "Listening",
                        "weight": "bold",
                        "size": "sm",
                        "wrap": True
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                              {
                                "type": "text",
                                "text": "1. ",
                                "margin": "none",
                                "size": "xs",
                                "flex": 0
                              },
                              {
                                "type": "text",
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5,
                                "text": article[0][1] +  '\n\n' + 'TOTAL: '+ article[0][4]
                              }
                            ],
                            "paddingAll": "10px"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                              {
                                "type": "text",
                                "text": "2. ",
                                "margin": "none",
                                "size": "xs",
                                "flex": 0
                              },
                              {
                                "type": "text",
                                "text": article[1][1] + '\n\n' + 'TOTAL: '+ article[1][4],
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                              }
                            ],
                            "paddingAll": "10px"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                              {
                                "type": "text",
                                "text": "3. ",
                                "margin": "none",
                                "size": "xs",
                                "flex": 0
                              },
                              {
                                "type": "text",
                                "text": article[2][1] + '\n\n' + 'TOTAL: '+ article[2][4],
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                              }
                            ],
                            "flex": 5,
                            "paddingAll": "10px"
                          }
                        ]
                      }
                    ],
                    "spacing": "sm",
                    "paddingAll": "10px"
                  }
                },
                {
                  "type": "bubble",
                  "size": "mega",
                  "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "Speaking",
                        "weight": "bold",
                        "size": "sm",
                        "wrap": True
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                              {
                                "type": "text",
                                "text": "1. ",
                                "margin": "none",
                                "size": "xs",
                                "flex": 0
                              },
                              {
                                "type": "text",
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5,
                                "text": article[0][2] + '\n\n' + 'TOTAL: '+ article[0][4]
                              }
                            ],
                            "paddingAll": "10px"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                              {
                                "type": "text",
                                "text": "2. ",
                                "margin": "none",
                                "size": "xs",
                                "flex": 0
                              },
                              {
                                "type": "text",
                                "text": article[1][2] + '\n\n' + 'TOTAL: '+ article[1][4],
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                              }
                            ],
                            "paddingAll": "10px"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                              {
                                "type": "text",
                                "text": "3. ",
                                "margin": "none",
                                "size": "xs",
                                "flex": 0
                              },
                              {
                                "type": "text",
                                "text": article[2][2] + '\n\n' + 'TOTAL: '+ article[2][4],
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                              }
                            ],
                            "flex": 5,
                            "paddingAll": "10px"
                          }
                        ]
                      }
                    ],
                    "spacing": "sm",
                    "paddingAll": "10px"
                  }
                },
                {
                  "type": "bubble",
                  "size": "mega",
                  "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "Writing",
                        "weight": "bold",
                        "size": "sm",
                        "wrap": True
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                              {
                                "type": "text",
                                "text": "1. ",
                                "margin": "none",
                                "size": "xs",
                                "flex": 0
                              },
                              {
                                "type": "text",
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5,
                                "text": article[0][3] +  '\n\n' + 'TOTAL: '+ article[0][4]
                              }
                            ],
                            "paddingAll": "10px"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                              {
                                "type": "text",
                                "text": "2. ",
                                "margin": "none",
                                "size": "xs",
                                "flex": 0
                              },
                              {
                                "type": "text",
                                "text": article[1][3] + '\n\n' + 'TOTAL: '+ article[1][4],
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                              }
                            ],
                            "paddingAll": "10px"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                              {
                                "type": "text",
                                "text": "3. ",
                                "margin": "none",
                                "size": "xs",
                                "flex": 0
                              },
                              {
                                "type": "text",
                                "text": article[2][3] + '\n\n' + 'TOTAL: '+ article[2][4],
                                "wrap": True,
                                "color": "#8c8c8c",
                                "size": "xs",
                                "flex": 5
                              }
                            ],
                            "flex": 5,
                            "paddingAll": "10px"
                          }
                        ]
                      }
                    ],
                    "spacing": "sm",
                    "paddingAll": "10px"
                  }
                }
              ]
            }
        ),
        line_bot_api.reply_message(event.reply_token, flex_message)
    
    
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))



'''
{
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "micro",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "Reading",
            "weight": "bold",
            "size": "sm",
            "wrap": true
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "1. ",
                    "margin": "none",
                    "size": "xs",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "獨立衝刺班寫作老師教我們用wordbank想點很有用我自己平時也會看高分同學的範文在看範文時可以先讀題在分鐘內想一想如果是自己會怎麼寫再去看高分文章效果會比較好整合關鍵是在聽力前面閱讀部分可以把個重點快速抄下不須抄太多聽力部分要注意聽盡量多抄平時要把轉折詞以及首尾段的寫法練熟考試時才可以花更多時間在內容的充實上",
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ]
              },
              {
                "type": "separator",
                "margin": "10px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "2. ",
                    "margin": "none",
                    "size": "xs",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "獨立衝刺班寫作老師教我們用wordbank想點很有用我自己平時也會看高分同學的範文在看範文時可以先讀題在分鐘內想一想如果是自己會怎麼寫再去看高分文章效果會比較好整合關鍵是在聽力前面閱讀部分可以把個重點快速抄下不須抄太多聽力部分要注意聽盡量多抄平時要把轉折詞以及首尾段的寫法練熟考試時才可以花更多時間在內容的充實上",
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ],
                "offsetTop": "10px"
              },
              {
                "type": "separator",
                "margin": "10px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "3. ",
                    "margin": "none",
                    "size": "xs",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "獨立衝刺班寫作老師教我們用wordbank想點很有用我自己平時也會看高分同學的範文在看範文時可以先讀題在分鐘內想一想如果是自己會怎麼寫再去看高分文章效果會比較好整合關鍵是在聽力前面閱讀部分可以把個重點快速抄下不須抄太多聽力部分要注意聽盡量多抄平時要把轉折詞以及首尾段的寫法練熟考試時才可以花更多時間在內容的充實上",
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ],
                "offsetTop": "10px"
              }
            ]
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    },
    {
      "type": "bubble",
      "size": "micro",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "Listening",
            "weight": "bold",
            "size": "sm",
            "wrap": true
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "1. ",
                    "margin": "none",
                    "size": "xs",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "獨立衝刺班寫作老師教我們用wordbank想點很有用我自己平時也會看高分同學的範文在看範文時可以先讀題在分鐘內想一想如果是自己會怎麼寫再去看高分文章效果會比較好整合關鍵是在聽力前面閱讀部分可以把個重點快速抄下不須抄太多聽力部分要注意聽盡量多抄平時要把轉折詞以及首尾段的寫法練熟考試時才可以花更多時間在內容的充實上",
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ]
              },
              {
                "type": "separator",
                "margin": "10px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "2. ",
                    "margin": "none",
                    "size": "xs",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "獨立衝刺班寫作老師教我們用wordbank想點很有用我自己平時也會看高分同學的範文在看範文時可以先讀題在分鐘內想一想如果是自己會怎麼寫再去看高分文章效果會比較好整合關鍵是在聽力前面閱讀部分可以把個重點快速抄下不須抄太多聽力部分要注意聽盡量多抄平時要把轉折詞以及首尾段的寫法練熟考試時才可以花更多時間在內容的充實上",
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ],
                "offsetTop": "10px"
              },
              {
                "type": "separator",
                "margin": "10px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "3. ",
                    "margin": "none",
                    "size": "xs",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "獨立衝刺班寫作老師教我們用wordbank想點很有用我自己平時也會看高分同學的範文在看範文時可以先讀題在分鐘內想一想如果是自己會怎麼寫再去看高分文章效果會比較好整合關鍵是在聽力前面閱讀部分可以把個重點快速抄下不須抄太多聽力部分要注意聽盡量多抄平時要把轉折詞以及首尾段的寫法練熟考試時才可以花更多時間在內容的充實上",
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ],
                "offsetTop": "10px"
              }
            ]
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    },
    {
      "type": "bubble",
      "size": "micro",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "Speaking",
            "weight": "bold",
            "size": "sm",
            "wrap": true
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "1. ",
                    "margin": "none",
                    "size": "xs",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "獨立衝刺班寫作老師教我們用wordbank想點很有用我自己平時也會看高分同學的範文在看範文時可以先讀題在分鐘內想一想如果是自己會怎麼寫再去看高分文章效果會比較好整合關鍵是在聽力前面閱讀部分可以把個重點快速抄下不須抄太多聽力部分要注意聽盡量多抄平時要把轉折詞以及首尾段的寫法練熟考試時才可以花更多時間在內容的充實上",
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ]
              },
              {
                "type": "separator",
                "margin": "10px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "2. ",
                    "margin": "none",
                    "size": "xs",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "獨立衝刺班寫作老師教我們用wordbank想點很有用我自己平時也會看高分同學的範文在看範文時可以先讀題在分鐘內想一想如果是自己會怎麼寫再去看高分文章效果會比較好整合關鍵是在聽力前面閱讀部分可以把個重點快速抄下不須抄太多聽力部分要注意聽盡量多抄平時要把轉折詞以及首尾段的寫法練熟考試時才可以花更多時間在內容的充實上",
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ],
                "offsetTop": "10px"
              },
              {
                "type": "separator",
                "margin": "10px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "3. ",
                    "margin": "none",
                    "size": "xs",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "獨立衝刺班寫作老師教我們用wordbank想點很有用我自己平時也會看高分同學的範文在看範文時可以先讀題在分鐘內想一想如果是自己會怎麼寫再去看高分文章效果會比較好整合關鍵是在聽力前面閱讀部分可以把個重點快速抄下不須抄太多聽力部分要注意聽盡量多抄平時要把轉折詞以及首尾段的寫法練熟考試時才可以花更多時間在內容的充實上",
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ],
                "offsetTop": "10px"
              }
            ]
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    },
    {
      "type": "bubble",
      "size": "micro",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "Writing",
            "weight": "bold",
            "size": "sm",
            "wrap": true
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "1. ",
                    "margin": "none",
                    "size": "xs",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "獨立衝刺班寫作老師教我們用wordbank想點很有用我自己平時也會看高分同學的範文在看範文時可以先讀題在分鐘內想一想如果是自己會怎麼寫再去看高分文章效果會比較好整合關鍵是在聽力前面閱讀部分可以把個重點快速抄下不須抄太多聽力部分要注意聽盡量多抄平時要把轉折詞以及首尾段的寫法練熟考試時才可以花更多時間在內容的充實上",
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ]
              },
              {
                "type": "separator",
                "margin": "10px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "2. ",
                    "margin": "none",
                    "size": "xs",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "獨立衝刺班寫作老師教我們用wordbank想點很有用我自己平時也會看高分同學的範文在看範文時可以先讀題在分鐘內想一想如果是自己會怎麼寫再去看高分文章效果會比較好整合關鍵是在聽力前面閱讀部分可以把個重點快速抄下不須抄太多聽力部分要注意聽盡量多抄平時要把轉折詞以及首尾段的寫法練熟考試時才可以花更多時間在內容的充實上",
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ],
                "offsetTop": "10px"
              },
              {
                "type": "separator",
                "margin": "10px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "3. ",
                    "margin": "none",
                    "size": "xs",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "獨立衝刺班寫作老師教我們用wordbank想點很有用我自己平時也會看高分同學的範文在看範文時可以先讀題在分鐘內想一想如果是自己會怎麼寫再去看高分文章效果會比較好整合關鍵是在聽力前面閱讀部分可以把個重點快速抄下不須抄太多聽力部分要注意聽盡量多抄平時要把轉折詞以及首尾段的寫法練熟考試時才可以花更多時間在內容的充實上",
                    "wrap": true,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ],
                "offsetTop": "10px"
              }
            ]
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    }
  ]
}

'''