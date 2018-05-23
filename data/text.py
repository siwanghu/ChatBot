# -*- coding: utf-8 -*-
import re  

def extract_chinese(intput_str):  
    match = re.compile('[^\u4e00-\u9fa5]')   
    chinese = " ".join(match.split(intput_str)).strip()  
    chinese = ",".join(chinese.split())  
    return chinese.split(",")[0]

def extract_info():
    with open("./uk_chat_message.sql","rb") as file_read:
        with open("./text.txt","w",encoding="utf-8") as file_write:
            line=file_read.readline()
            line=str(line,"utf-8")
            while line:
                if "in" in line:
                    obj="in"
                else:
                    obj="out"
                    obj=obj+" "+extract_chinese(line)+"\n"
                    line=file_read.readline()
                    line=str(line,"utf-8")
                    file_write.writelines(obj)

def get_info():
    with open("./text.txt","rb") as file_read:
        with open("./info.txt","w",encoding="utf-8") as file_write:
            line=file_read.readline()
            line=str(line,"utf-8")
            write=""
            flag="out"
            while line:
                if flag in line:
                    write=write+extract_chinese(line)
                else:
                    file_write.writelines(flag+" "+write+"\n")
                    write=""
                    write=write+extract_chinese(line)
                    if "in" in line:
                        flag="in"
                    else:
                        flag="out"
                line=file_read.readline()
                line=str(line,"utf-8")

def divide_info():
    with open("./info.txt","rb") as file_read:
        with open("./question","w",encoding="utf-8") as file_question:
            with open("./answer","w",encoding="utf-8") as file_answer:
                line=file_read.readline()
                line=str(line,"utf-8")
                while line:
                    if "in" in line:
                        file_question.writelines(extract_chinese(line)+"\n")
                    elif "out" in line:
                        file_answer.writelines(extract_chinese(line)+"\n")
                    line=file_read.readline()
                    line=str(line,"utf-8")

divide_info()