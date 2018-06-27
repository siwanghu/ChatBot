# -*- coding: utf-8 -*-
import os
import re
import requests

def dowmloadPic(html, keyword):
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    i = 1
    for each in pic_url:
        print('正在下载第' + str(i) + '张图片：')
        try:
            pic = requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            continue

        dir = str(i) + '.jpg'
        fp = open(dir, 'wb')
        fp.write(pic.content)
        fp.close()
        i += 1

if __name__ == '__main__':
    os.chdir("C:\\Users\siwanghu\Desktop\images")
    word = input("Input key word: ")
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip'
    result = requests.get(url)
    dowmloadPic(result.text, word)