# -*- coding: utf-8 -*-
import re  
import os
import json
import nltk
import jieba
import analyse
import numpy
import matplotlib.pyplot as plt
from gensim import models
from sklearn.cluster import KMeans
from stanfordcorenlp import StanfordCoreNLP 

def extract_chinese(intput_str):  
    match = re.compile('[^\u4e00-\u9fa5]')   
    chinese = " ".join(match.split(intput_str)).strip()  
    chinese = ",".join(chinese.split())  
    return chinese.split(",")[0]

def extract_info():
    with open("./data/uk_chat_message.sql","rb") as file_read:
        with open("./data/text.txt","w",encoding="utf-8") as file_write:
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
                print(obj)
                file_write.writelines(obj)

def get_info():
    with open("./data/text.txt","rb") as file_read:
        with open("./data/info.txt","w",encoding="utf-8") as file_write:
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
    with open("./data/text.txt","rb") as file_read:
        with open("./data/question.txt","w",encoding="utf-8") as file_question:
            with open("./data/answer.txt","w",encoding="utf-8") as file_answer:
                line=file_read.readline()
                line=str(line,"utf-8")
                while line:
                    if "in" in line and len(extract_chinese(line))>3:
                        file_question.writelines(extract_chinese(line)+"\n")
                    elif "out" in line and len(extract_chinese(line))>3:
                        file_answer.writelines(extract_chinese(line)+"\n")
                    line=file_read.readline()
                    line=str(line,"utf-8")

def jsonParse():
    with open("./data/myfile.txt","w",encoding="utf-8") as file_obj:
        dicts=json.load(open("./data/qafile.txt",encoding="utf-8"))
        for qa in dicts:
            file_obj.writelines(qa["queation"]+"\n")
            file_obj.writelines(qa["answer"]+"\n")
            
def word_frequency():
    result_word=[]
    stop_word=["\r\n","\n"]
    with open("./data/stopwords.txt","rb") as file_read:
        line=file_read.readline()
        line=str(line,"utf-8").replace("\r\n","").replace("\n","")
        while line:
            stop_word.append(line)
            line=file_read.readline()
            line=str(line,"utf-8").replace("\r\n","").replace("\n","")
    with open("./data/info.txt","rb") as file_read:
        line=file_read.readline()
        line=str(line,"utf-8")
        while line:
            for word in jieba.cut(line):
                if word not in stop_word:
                    result_word.append(word)
            line=file_read.readline()
            line=str(line,"utf-8")
        result=nltk.probability.FreqDist(result_word)
    return result

def show_frequency():
    frequency=word_frequency().most_common(50)
    for word in frequency:
        print(word)
    X=range(len([x for (x,y) in frequency]))
    Y=[y for (x,y) in frequency]
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('词频统计图') 
    plt.plot(X,Y)
    plt.show()
    
def cluster(n_clusters=25):
    result=[]
    model = models.Word2Vec.load("./word2vec/word2vec_model")
    frequency=word_frequency().most_common(50)
    features=[model[x] for (x,y) in frequency]
    k_means = KMeans(n_clusters=n_clusters)
    k_model=k_means.fit(features)
    for index in range(len(k_model.labels_)):
        result.append((k_model.labels_[index],frequency[index][0]))
    list.sort(result)
    dicts,clusters={},n_clusters
    for _ in range(clusters):
        dicts[_]=[]
    for result in result:
        dicts[result[0]].append(result[1])
    for key,value in dicts.items():
        print("第"+str(key+1)+"类： ",value)
        
def create_file():
    path=r"C:\Users\siwanghu\Desktop\chatbot\data\split_question"
    os.chdir(path)
    frequency=word_frequency().most_common(50)
    for word in frequency:
        word=word[0]
        print("处理: ",word)
        file=open(word+".txt","w")
        file.close()
        
def split_question():
    path=r"C:\Users\siwanghu\Desktop\chatbot\data\split_question"
    frequency=word_frequency().most_common(50)
    for word in frequency:
        word=word[0]
        print("处理: ",word)
        with open("./data/question.txt","rb") as file_read:
            with open(path+"\\"+word+".txt","w",encoding="utf-8") as file_writer:
                line=file_read.readline()
                line=str(line,"utf-8")
                while line:
                    words=jieba.cut(line)
                    words=[key for key in words]
                    if word in words:
                        file_writer.writelines(line)
                    line=file_read.readline()
                    line=str(line,"utf-8")

def cluster_question(n_clusters=30):
    result=[]
    lines=[]
    model = models.Word2Vec.load("./word2vec/word2vec_model")
    with open("./data/split_question/产品.txt","rb") as file:
        line=file.readline()
        line=str(line,"utf-8").replace("\r\n","").replace("\n","").replace("\r","")
        while line:
            words=analyse.extract_keyword(line)
            try:
                keys=numpy.array([model[word] for word in words])
            except:
                line=file.readline()
                line=str(line,"utf-8").replace("\r\n","").replace("\n","").replace("\r","")
                continue
            keys=numpy.sum(keys,axis=0)/len(words)
            lines.append((line,keys))
            line=file.readline()
            line=str(line,"utf-8").replace("\r\n","").replace("\n","").replace("\r","")
    features=[y for (x,y) in lines]
    k_means = KMeans(n_clusters=n_clusters)
    k_model=k_means.fit(features)
    for index in range(len(k_model.labels_)):
        result.append((k_model.labels_[index],lines[index][0]))
    list.sort(result)
    dicts,clusters={},n_clusters
    for _ in range(clusters):
        dicts[_]=[]
    for result in result:
        dicts[result[0]].append(result[1])
    for key,value in dicts.items():
        print("第"+str(key+1)+"类： ",value[0:2])
    
def stanford_nlp(input_str):
    nlp=StanfordCoreNLP(r"C:\Users\siwanghu\Desktop\stanford-corenlp-full",lang="zh")
    return (nlp.word_tokenize(input_str),\
            nlp.pos_tag(input_str),\
            nlp.ner(input_str),\
            nlp.parse(input_str),\
            nlp.dependency_parse(input_str))

cluster_question()