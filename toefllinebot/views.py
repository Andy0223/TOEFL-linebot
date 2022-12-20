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
#取得settings.py中的LINE Bot憑證來進行Messaging API的驗證
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

global result

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
                    func.backgroundconfirmbutton(event)
                    
                elif event.message.text.split('\n')[0] == "mygoal":
                    
                    func.goalconfirmbutton(event)
                
            if isinstance(event, PostbackEvent):
                backdata = dict(parse_qsl(event.postback.data))
                #print(parse_qsl(event.postback.data))
                backgroundinfo = "請輸入您的背景(多益/學測/指考):\n\n範例格式:\n1.\nmybackground\n800/14/82\n2.\nmybackground\n700//10\n\n請按照格式輸入，mybackground後要下一行，無分數可不用輸入，如範例二"
                goalinfo = "請問你的目標總分為何? (70~120分)\n\n範例格式:\n1.\nmygoal\n100\n\n2.\nmygoal\n85"
                
                if backdata.get('action') == 'backgroundyes':
                    func.backgroundmessage(event)
                
                #backgroundskip or backgroundtrue
                elif event.postback.data[0:1] == "A":
                    background = event.postback.data[2:]
                    func.goalmessage(event,background)

                elif event.postback.data[0:1] == "B":
                    print("background:",event.postback.data)
                elif backdata.get('action') == 'backgroundfalse':
                    func.backgroundmessage(event)
                elif backdata.get('action') == 'goaltrue':
                    #article type
                    func.typebutton(event)
                elif backdata.get('action') == 'goalfalse':
                    #goal
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=goalinfo))
                '''elif backdata.get('action') == 'selftaught':
                    
                elif backdata.get('action') == 'cram':'''
                
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

