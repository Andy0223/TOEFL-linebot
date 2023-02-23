from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage,FlexSendMessage
from LineBot.summ import summary

import requests
import re
import math
from LineBot.classification import Insert,dbQuery,dbQueryPercentage,dbInsertUser


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    global temp
    global feature
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
            UserId = event.source.user_id
            UserName = line_bot_api.get_profile(UserId).display_name
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.text == "心得摘要":
                    temp = event.message.text
                    feature = event.message.text
                    summary(event)
                elif event.message.text == "學習歷程":
                    temp = event.message.text
                    feature = event.message.text
                    print("feature",feature)
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=f'{UserName}歡迎！\n\n請輸入您欲使用的功能\n\n> 查詢日記\n> 各科分佈\n> 新增日記'))
                elif event.message.text == "關閉":
                    temp = event.message.text
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Goodbye'))
                else:
                    # feature = event.message.text
                    # line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請打開選單點選您欲使用的功能'))

                    if feature == "心得摘要" and event.message.text != "心得摘要":
                        summary(event)
                    elif feature == "學習歷程" and event.message.text != "學習歷程":
                        # temp = event.message.text
                        if(event.message.text == ("關閉" or "stop" or "Stop")):
                            temp = event.message.text
                            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Goodbye'))
                        elif("各科分佈" in event.message.text):
                            temp = event.message.text
                            data,total = dbQueryPercentage(UserId)
                            if(data == "你尚未建立任何學習歷程，請輸入『新增日記』"):
                                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=data))
                            elif(data == "無法查詢，請重新輸入"):
                                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=data))
                            else:
                                reply = []
                                carousel = []
                                for k,v in data.items():
                                    carousel.append(
                                        {
                                            "type": "bubble",
                                            "size": "nano",
                                            "header": {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [
                                                {
                                                    "type": "text",
                                                    "text": f"{k} 共{v}篇",
                                                    "color": "#ffffff",
                                                    "align": "start",
                                                    "size": "md",
                                                    "gravity": "center"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": f"{round(v/total,2)*100}%",
                                                    "color": "#ffffff",
                                                    "align": "start",
                                                    "size": "xs",
                                                    "gravity": "center",
                                                    "margin": "lg"
                                                },
                                                {
                                                    "type": "box",
                                                    "layout": "vertical",
                                                    "contents": [
                                                    {
                                                        "type": "box",
                                                        "layout": "vertical",
                                                        "contents": [
                                                        {
                                                            "type": "filler"
                                                        }
                                                        ],
                                                        "width": f"{round(v/total,1)*100}%",
                                                        "backgroundColor": "#0D8186",
                                                        "height": "6px"
                                                    }
                                                    ],
                                                    "backgroundColor": "#9FD8E36E",
                                                    "height": "6px",
                                                    "margin": "sm"
                                                }
                                                ],
                                                "backgroundColor": "#27ACB2",
                                                "paddingTop": "19px",
                                                "paddingAll": "12px",
                                                "paddingBottom": "16px"
                                            }
                                        }
                                    )
                            reply.append(FlexSendMessage(alt_text="請查看各科分佈",contents={"type":"carousel","contents":carousel}))
                            reply.append(TextSendMessage(text='請問您還想使用哪個功能呢？\n\n> 查詢日記\n> 各科分佈\n> 新增日記'))
                            line_bot_api.reply_message(event.reply_token,reply)
                        elif("查詢" in event.message.text):
                            temp = event.message.text
                            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請問你想要查詢什麼科目的日記呢？\n(閱讀、聽力、口說、寫作)'))
                        elif("新增" in event.message.text):
                            temp = event.message.text
                            print(temp)
                            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='歡迎在底下留言紀錄自己的成長歷程'))
                        elif("閱讀" == event.message.text):
                            temp = event.message.text
                            data,dt = dbQuery("閱讀",UserId)
                            if(data == "無法查詢，請重新輸入"):
                                reply = []
                                reply.append(TextSendMessage(text=f'您尚未新增過閱讀日記，請輸入『新增日記』開始記錄'))
                                reply.append(TextSendMessage(text=f'請問還要看哪一個科目？\n\n(閱讀、聽力、口說、寫作)'))
                                reply.append(TextSendMessage(text='或是請輸入您欲使用的功能\n\n> 查詢日記\n> 各科分佈\n> 新增日記'))
                                line_bot_api.reply_message(event.reply_token,reply)
                            else:
                                reply = []
                                carousel = []
                                for i,item in enumerate(data):
                                    carousel.append(
                                        {
                                            "type": "bubble",
                                            "header": {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": f"{temp} {i+1}",
                                                        "weight": "bold",
                                                        "align": "center",
                                                        "size": "xl"
                                                    }
                                                ]
                                            },
                                            "hero": {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": f"{dt[i]}",
                                                        "align": "center",
                                                        "wrap": True
                                                    }
                                                ]
                                            },
                                            "body": {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": f"{item}",
                                                        "wrap": True
                                                    }
                                                ]
                                            }
                                        }
                                    )
                                reply.append(FlexSendMessage(alt_text=f"請查看{event.message.text}日記",contents={"type":"carousel","contents":carousel}))
                                reply.append(TextSendMessage(text=f'請問還要看哪一個科目？\n\n(閱讀、聽力、口說、寫作)'))
                                reply.append(TextSendMessage(text='或是請輸入您欲使用的功能\n\n> 查詢日記\n> 各科分佈\n> 新增日記'))
                                line_bot_api.reply_message(event.reply_token,reply)
                        elif("聽力" == event.message.text):
                            temp = event.message.text
                            data,dt = dbQuery("聽力",UserId)
                            if(data == "無法查詢，請重新輸入"):
                                reply = []
                                reply.append(TextSendMessage(text=f'您尚未新增過聽力日記，請輸入『新增日記』開始記錄'))
                                reply.append(TextSendMessage(text=f'請問還要看哪一個科目？\n\n(閱讀、聽力、口說、寫作)'))
                                reply.append(TextSendMessage(text='或是請輸入您欲使用的功能\n\n> 查詢日記\n> 各科分佈\n> 新增日記'))
                                line_bot_api.reply_message(event.reply_token,reply)
                            else:
                                reply = []
                                carousel = []
                                for i,item in enumerate(data):
                                    carousel.append(
                                        {
                                            "type": "bubble",
                                            "header": {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": f"{temp} {i+1}",
                                                        "weight": "bold",
                                                        "align": "center",
                                                        "size": "xl"
                                                    }
                                                ]
                                            },
                                            "hero": {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": f"{dt[i]}",
                                                        "align": "center",
                                                        "wrap": True
                                                    }
                                                ]
                                            },
                                            "body": {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": f"{item}",
                                                        "wrap": True
                                                    }
                                                ]
                                            }
                                        }
                                    )
                                reply.append(FlexSendMessage(alt_text=f"請查看{event.message.text}日記",contents={"type":"carousel","contents":carousel}))
                                reply.append(TextSendMessage(text=f'請問還要看哪一個科目？\n\n(閱讀、聽力、口說、寫作)'))
                                reply.append(TextSendMessage(text='或是請輸入您欲使用的功能\n\n> 查詢日記\n> 各科分佈\n> 新增日記'))
                                line_bot_api.reply_message(event.reply_token,reply)
                        elif("口說" == event.message.text):
                            temp = event.message.text
                            data,dt = dbQuery("口說",UserId)
                            if(data == "無法查詢，請重新輸入"):
                                reply = []
                                reply.append(TextSendMessage(text=f'您尚未新增過口說日記，請輸入『新增日記』開始記錄'))
                                reply.append(TextSendMessage(text=f'請問還要看哪一個科目？\n\n(閱讀、聽力、口說、寫作)'))
                                reply.append(TextSendMessage(text='或是請輸入您欲使用的功能\n\n> 查詢日記\n> 各科分佈\n> 新增日記'))
                                line_bot_api.reply_message(event.reply_token,reply)
                            else:
                                reply = []
                                carousel = []
                                for i,item in enumerate(data):
                                    carousel.append(
                                        {
                                            "type": "bubble",
                                            "header": {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": f"{temp} {i+1}",
                                                        "weight": "bold",
                                                        "align": "center",
                                                        "size": "xl"
                                                    }
                                                ]
                                            },
                                            "hero": {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": f"{dt[i]}",
                                                        "align": "center",
                                                        "wrap": True
                                                    }
                                                ]
                                            },
                                            "body": {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": f"{item}",
                                                        "wrap": True
                                                    }
                                                ]
                                            }
                                        }
                                    )
                                reply.append(FlexSendMessage(alt_text=f"請查看{event.message.text}日記",contents={"type":"carousel","contents":carousel}))
                                reply.append(TextSendMessage(text=f'請問還要看哪一個科目？\n\n(閱讀、聽力、口說、寫作)'))
                                reply.append(TextSendMessage(text='或是請輸入您欲使用的功能\n\n> 查詢日記\n> 各科分佈\n> 新增日記'))
                                line_bot_api.reply_message(event.reply_token,reply)
                        elif("寫作" == event.message.text):
                            temp = event.message.text
                            data,dt = dbQuery("寫作",UserId)
                            if(data == "無法查詢，請重新輸入"):
                                reply = []
                                reply.append(TextSendMessage(text=f'您尚未新增過寫作日記，請輸入『新增日記』開始記錄'))
                                reply.append(TextSendMessage(text=f'請問還要看哪一個科目？\n\n(閱讀、聽力、口說、寫作)'))
                                reply.append(TextSendMessage(text='或是請輸入您欲使用的功能\n\n> 查詢日記\n> 各科分佈\n> 新增日記'))
                                line_bot_api.reply_message(event.reply_token,reply)
                            else:
                                reply = []
                                carousel = []
                                for i,item in enumerate(data):
                                    carousel.append(
                                        {
                                            "type": "bubble",
                                            "header": {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": f"{temp} {i+1}",
                                                        "weight": "bold",
                                                        "align": "center",
                                                        "size": "xl"
                                                    }
                                                ]
                                            },
                                            "hero": {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": f"{dt[i]}",
                                                        "align": "center",
                                                        "wrap": True
                                                    }
                                                ]
                                            },
                                            "body": {
                                                "type": "box",
                                                "layout": "horizontal",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": f"{item}",
                                                        "wrap": True
                                                    }
                                                ]
                                            }
                                        }
                                    )
                                reply.append(FlexSendMessage(alt_text=f"請查看{event.message.text}日記",contents={"type":"carousel","contents":carousel}))
                                reply.append(TextSendMessage(text=f'請問還要看哪一個科目？\n\n(閱讀、聽力、口說、寫作)'))
                                reply.append(TextSendMessage(text='或是請輸入您欲使用的功能\n\n> 查詢日記\n> 各科分佈\n> 新增日記'))
                                line_bot_api.reply_message(event.reply_token,reply)
                        else:
                            print(temp)
                            if("新增" in temp):
                                if len(event.message.text) < 10:
                                    reply = []
                                    reply.append(TextSendMessage(text='不好意思，我無法理解您的需求'))
                                    reply.append(TextSendMessage(text='請重新輸入您欲使用的功能\n\n> 查詢日記\n> 各科分佈\n> 新增日記'))
                                    line_bot_api.reply_message(event.reply_token,reply)
                                else:
                                    dbInsertUser(UserName,UserId)
                                    data = Insert(event.message.text,UserId)
                                    reply = []
                                    reply.append(TextSendMessage(text=f'{data}'))
                                    reply.append(TextSendMessage(text='請輸入您欲使用的功能\n\n> 查詢日記\n> 各科分佈\n> 新增日記'))
                                    line_bot_api.reply_message(event.reply_token,reply)
                            else:
                                temp = event.message.text
                                reply = []
                                reply.append(TextSendMessage(text='不好意思，我無法理解您的需求'))
                                reply.append(TextSendMessage(text='請重新輸入您欲使用的功能\n\n> 查詢日記\n> 各科分佈\n> 新增日記'))
                                line_bot_api.reply_message(event.reply_token,reply)
            else:
                if feature == "心得摘要":
                    summary(event)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()