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
    PostbackTemplateAction
)

#取得settings.py中的LINE Bot憑證來進行Messaging API的驗證
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
def startbutton(event):
    try:
        message = TemplateSendMessage(
            alt_text = '按鈕樣板',
            template = ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/pRdaAmS.jpg',
                title='歡迎使用托福linebot',
                text='請選擇是否開始使用：',
                actions=[
                    MessageTemplateAction(
                        label='start',
                        text='start'
                    ),
                    MessageTemplateAction(
                        label='stop',
                        text='stop'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
def backgroundbutton(event):
    try:
        '''message = TemplateSendMessage(
            alt_text = '按鈕樣板',
            template = ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/pRdaAmS.jpg',
                title='背景調查',
                text='請問您的英文背景：',
                actions=[
                    MessageTemplateAction(
                        label='開始輸入',
                        text='@start input'
                    )
                ]
            )
        )'''
        Confirm_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ConfirmTemplate(
            title='是否提供您的背景',
            text='是否提供您的背景?\n我們可以搜尋到跟您背景類似的心得文',
            actions=[                              
                PostbackTemplateAction(
                    label='Yes',
                    text='Yes',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='Skip',
                    text='Skip'
                )
            ]
        )
        )
        line_bot_api.reply_message(event.reply_token,Confirm_template)
        
        '''backgroundinfo = "請輸入您的背景(多益/學測/指考):\n範例一: 800/14/82\n範例二: 700//10\n請按照格式輸入，無分數可不用輸入，如範例二"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=backgroundinfo))'''
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))



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
                if event.message.text == "start":
                    backgroundbutton(event)
                elif event.message.text == "stop":
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='goodbye'))
                elif event.message.text == "@start input":
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='您的背景是否正確'))
                else:
                    startbutton(event)
            if isinstance(event, PostbackEvent):
                backdata = dict(parse_qsl(event.postback.data))
                if backdata.get('action') == '第一隻喵':
                    func.sendBack_cat01(event, backdata)
                elif backdata.get('action') == '第二隻喵':
                    func.sendBack_cat02(event,backdata)
                elif backdata.get('action') == '第三隻喵':
                    func.sendBack_cat03(event,backdata)
               
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

