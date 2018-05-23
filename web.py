# -*- coding: utf-8 -*-
import os
import aiml
import analyse
from flask import Flask, request, jsonify
from train import predict_from_network

ret,num=[],0
app = Flask(__name__)

@app.route('/tensorflow',methods=["GET"])
def predict_tensorflow():
    global ret,num
    if not request.args or "input" not in request.args:
        ret,num=[],0
        return jsonify({"result":"error"})
    else:
        input_str = preproccess_str(request.args["input"])
        if len(input_str)==0:
            ret,num=[],0
            return ""
        else:
            print("原始: "+input_str)
            input_str=similarity(input_str)
            result="请直接说出你的问题"
            if len(input_str)==0:
                print("输出: " + result)
                return jsonify({"result":result})
            print("输入: "+input_str)
            result = predict_from_network(input_str).replace(" ","")
            print("输出: " + result)
            ret,num=[],0
            return jsonify({"result":result})

@app.route('/aiml',methods=["GET"])
def predict_aiml():
    global ret,num
    if not request.args or "input" not in request.args:
        ret,num=[],0
        return jsonify({"result":"error"})
    else:
        input_str = preproccess_str(request.args["input"])
        result=mybot.respond(input_str)
        if result:
            return jsonify({"result":result})
        else:
            if len(input_str)==0:
                ret,num=[],0
                return ""
            else:                        
                print("原始: "+input_str)
                input_str=similarity(input_str)
                result="请直接说出你的问题"
                if len(input_str)==0:
                    print("输出: " + result)
                    return jsonify({"result":result})
                print("输入: "+input_str)
                result=mybot.respond(input_str)
                print("输出: " + result)
                ret,num=[],0
                return jsonify({"result":result})

def preproccess_str(input_str):
    return input_str.replace("。","").replace(",","").replace("？","").replace(" ","")

def similarity(input_str):
    global ret,num
    with open("../samples/question","rb") as file_obj:
        question=str(file_obj.readline(),"utf-8")
        while question:
            key_question=analyse.extract_keyword(question)
            key_input=analyse.extract_keyword(input_str)
            if len(set(key_question)&set(key_input))>num:
                ret=question
                num=len(set(key_question)&set(key_input))
            question=str(file_obj.readline(),"utf-8")
        return ret
        
if __name__ == "__main__":
    mybot_path = '.\mybot'
    os.chdir(mybot_path)
    print(mybot_path)
    mybot = aiml.Kernel()
    mybot.learn("std-startup.xml")
    mybot.respond('LOAD AIML C')
    app.run(host='0.0.0.0',port=5000,debug=False)