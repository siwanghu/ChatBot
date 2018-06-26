# -*- coding: utf-8 -*-
import itchat
import requests

key='b7505ed8dad24dc5942ebd5ae80dbd95'
apiUrl='http://www.tuling123.com/openapi/api'

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
    
itchat.auto_login()
itchat.run()