# -*- coding: utf-8 -*-
import os
import itchat
import requests
import random

key='b7505ed8dad24dc5942ebd5ae80dbd95'
apiUrl='http://www.tuling123.com/openapi/api'

def itchat_file(lists=[],path="./picture"):
    for file in os.listdir(path):
        file = path+"/"+file
        if os.path.isfile(file):
            lists.append(file)
    return random.choice(lists)

def get_response(msg):
    print("接收到消息:",msg)
    data = {'key': key,'info': msg, 'userid':'my-robot',}
    try:
        req=requests.post(apiUrl,data=data).json()
        return req.get('text')
    except:
        return

@itchat.msg_register(itchat.content.TEXT)
def return_text_content(msg):
    reply=get_response(msg['Text'])
    print(reply)
    return reply

@itchat.msg_register(itchat.content.PICTURE)
def return_picture_content(msg):
    itchat.send_image(itchat_file(),toUserName=msg['FromUserName'])
    print("发送成功")

itchat.auto_login()
itchat.run()