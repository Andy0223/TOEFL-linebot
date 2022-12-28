from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
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
from urllib.parse import parse_qsl
from . import func
import numpy as np
#取得settings.py中的LINE Bot憑證來進行Messaging API的驗證
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

result = {}

@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                #print(event.message.text.split('\n'))
                if event.message.text == "start":
                    
                    func.backgroundbutton(event)
                elif event.message.text == "stop":
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='goodbye'))
                elif event.message.text.split('\n')[0] == "mybackground":
                    score = event.message.text.split('\n')[1].split('/')
                    if score[0]=='':
                        tscore=''
                    else:
                        tscore=int(score[0])
                    if score[1]=='':
                        sscore=''
                    else:
                        sscore=int(score[1])
                    if score[2]=='':
                        jscore=''
                    else:
                        jscore=int(score[2])
                    if tscore!='' and (tscore>990 or tscore<0 or type(tscore)!=int) : 
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='多益成績範圍錯誤，請再輸入一次'))
                        #func.backgroundmessage_rangewrong(event)
                    elif sscore!='' and (sscore>15 or sscore<0 or type(sscore)!=int) :
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='學測成績範圍錯誤，請再輸入一次'))
                        #func.backgroundmessage_rangewrong(event)
                    elif jscore!='' and (jscore>100 or jscore<0):
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='指考成績範圍錯誤，請再輸入一次'))
                        #func.backgroundmessage_rangewrong(event)
                    else:
                        func.backgroundconfirmbutton(event)
                    
                    
                elif event.message.text.split('\n')[0] == "mygoal":
                    if (int(event.message.text.split('\n')[1])>120) or (int(event.message.text.split('\n')[1])<70):
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='範圍錯誤，請再輸入一次'))
                        func.goalmessage(event)
                    else:
                        func.goalconfirmbutton(event)
                '''else:
                    
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))'''
            if isinstance(event, PostbackEvent):
                backdata = dict(parse_qsl(event.postback.data))
                #print(parse_qsl(event.postback.data))
                backgroundinfo = "請輸入您的背景(多益/學測/指考):\n\n範例格式:\n1.\nmybackground\n800/14/82\n2.\nmybackground\n700//10\n\n請按照格式輸入，mybackground後要下一行，無分數可不用輸入，如範例二"
                goalinfo = "請問你的目標總分為何? (70~120分)\n\n範例格式:\n1.\nmygoal\n100\n\n2.\nmygoal\n85"
                
                if backdata.get('action') == 'backgroundyes':
                    func.backgroundmessage(event)
                
                elif backdata.get('action') == 'backgroundfalse':
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請再輸入一次'))
                    func.backgroundmessage(event)

                #backgroundskip or backgroundtrue
                elif event.postback.data[0:1] == "A":
                    background = event.postback.data[2:]
                    func.storevalue("background",background,result)
                    func.goalmessage(event)

                #goaltrue
                elif event.postback.data[0:1] == "B":
                    goal = event.postback.data[2:]
                    func.storevalue("goal",goal,result)
                    func.typebutton(event)
                
                elif backdata.get('action') == 'goalfalse':
                    #goal
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請再輸入一次'))
                    func.goalmessage(event)
                elif event.postback.data[0:1] == "C":
                    artype = event.postback.data[2:]
                    func.storevalue("type",artype,result)
                    func.subjectmessage(event,result)
                
                
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

