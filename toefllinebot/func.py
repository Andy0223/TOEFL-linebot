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
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


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
def backgroundconfirmbutton(event):
    try:
        score = event.message.text.split('\n')[1].split('/')
        #print(event.message.text)
        backgroundconfirmtext = 'so, your background is:\n'+"多益:"+score[0]+"分/學測:"+score[1]+"級/指考:"+score[2]+"分\n"+"是否正確:"
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
def goalmessage(event,background):
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
        goalconfirmtext = 'so, your goal is:\n'+score1+"\n"+"是否正確:"
        Confirm_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ConfirmTemplate(
            title='goal',
            text=goalconfirmtext,
            actions=[                              
                PostbackTemplateAction(
                    label='正確',
                    text='正確',
                    data='action=goaltrue'
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
                        data='action=selftaught'
                    ),
                    PostbackTemplateAction(
                        label='補習文',
                        text='補習文',
                        data='action=cram'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
