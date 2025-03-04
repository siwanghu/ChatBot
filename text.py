# -*- coding: utf-8 -*-
import re  
import os
import json
import nltk
import jieba
import analyse
import numpy,scipy
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from gensim import models
from sklearn.cluster import KMeans
from apyori import apriori
from stanfordcorenlp import StanfordCoreNLP 
from wordcloud import WordCloud

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
    with open("./stopwords.txt","rb") as file_read:
        line=file_read.readline()
        line=str(line,"utf-8").replace("\r\n","").replace("\n","")
        while line:
            stop_word.append(line)
            line=file_read.readline()
            line=str(line,"utf-8").replace("\r\n","").replace("\n","")
    with open("./info.txt","rb") as file_read:
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
    frequency=word_frequency().most_common(100)
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
    return dicts
        
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
    frequency=[x for (x,y) in frequency]
    dicts={}
    for word in frequency:
        dicts[word]=[]
    for word in frequency:
        print("处理: ",word)
        with open("./data/question.txt","rb") as file_read:
            line=file_read.readline()
            line=str(line,"utf-8")
            with open(path+"\\"+word+".txt","w",encoding="utf-8") as file_writer:
                line=file_read.readline()
                line=str(line,"utf-8")
                while line:
                    words=jieba.cut(line)
                    words=[key for key in words if key in frequency]
                    if word in words:
                        file_writer.writelines(line)
                    line=file_read.readline()
                    line=str(line,"utf-8")

def split_question2():
    path=r"C:\Users\siwanghu\Desktop\chatbot\data\split_question"
    frequency=word_frequency().most_common(50)
    frequency=[x for (x,y) in frequency]
    file_dicts={}
    for word in frequency:
        file_dicts[word]=open(path+"\\"+word+".txt","w",encoding="utf-8")
    with open("./data/question.txt","rb") as file_read:
        line=file_read.readline()
        line=str(line,"utf-8")
        print("处理....")
        while line:
            itrs=jieba.cut(line)
            words=[itr for itr in itrs if itr in frequency]
            for word in frequency:
                if word in words:
                    file_dicts[word].writelines(line)
                    break
            line=file_read.readline()
            line=str(line,"utf-8")
    for word in file_dicts.keys():
        file_dicts[word].close()

def cluster_question(file_name,n_clusters):
    result=[]
    lines=[]
    model = models.Word2Vec.load("./word2vec/word2vec_model")
    frequency=word_frequency().most_common(100)
    frequency=[x for (x,y) in frequency]
    file_writer=open("./data/split_question/"+file_name+"_聚类.txt","w")
    with open("./data/split_question/"+file_name+".txt","rb") as file:
        line=file.readline()
        line=str(line,"utf-8").replace("\r\n","").replace("\n","").replace("\r","")
        while line:
            words=analyse.__cut_word(line)
            extract=[]
            try:
                extract=[word for word in words if word in frequency]
                keys=numpy.array([model[word] for word in extract])
            except:
                line=file.readline()
                line=str(line,"utf-8").replace("\r\n","").replace("\n","").replace("\r","")
                continue
            keys=numpy.sum(keys,axis=0)/len(words)
            lines.append((line,keys,extract))
            line=file.readline()
            line=str(line,"utf-8").replace("\r\n","").replace("\n","").replace("\r","")
    features=[y for (x,y,z) in lines]
    k_means = KMeans(n_clusters=n_clusters)
    k_model=k_means.fit(features)
    ids=k_model.cluster_centers_
    for index in range(len(k_model.labels_)):
        result.append((k_model.labels_[index],lines[index][0]))
    list.sort(result)
    dicts,clusters={},n_clusters
    for _ in range(clusters):
        dicts[_]=[]
    for result in result:
        dicts[result[0]].append(result[1])
    for key,value in dicts.items():
        print("第"+str(key+1)+"类： ",value)
        file_writer.writelines("第"+str(key+1)+"类： "+str(value)+"\n")
        file_writer.writelines("语义向量："+str(ids[key])+"\n")
        file_writer.writelines("\n\n")
    file_writer.close()
    
def stanford_nlp(input_str):
    nlp=StanfordCoreNLP(r"C:\Users\siwanghu\Desktop\stanford-corenlp-full",lang="zh")
    return (nlp.word_tokenize(input_str),\
            nlp.pos_tag(input_str),\
            nlp.ner(input_str),\
            nlp.parse(input_str),\
            nlp.dependency_parse(input_str))

def get_file_size(file):
    fsize = os.path.getsize(file)
    fsize = fsize/float(1024)
    return int(fsize)+1

def cluster_all_question():
    frequency=word_frequency().most_common(50)
    frequency=[x for (x,y) in frequency]
    for word in frequency:
        fsize=get_file_size("./data/split_question/"+word+".txt")
        print("处理：",word,fsize)
        cluster_question(word,fsize)

def test_my_apyori():
    data=[['豆奶','莴苣'],\
          ['莴苣','尿布','葡萄酒','甜菜'],\
          ['豆奶','尿布','葡萄酒','橙汁'],\
          ['莴苣','豆奶','尿布','葡萄酒'],\
          ['莴苣','豆奶','尿布','橙汁']]
    result=list(apriori(transactions=data))
    print(result)

def drawWordCloud(seg_list):
    color_mask = scipy.misc.imread("./1.png")
    wc = WordCloud(
        font_path="simkai.ttf",
        background_color='white',
        mask=color_mask,
        max_words=50,
        max_font_size=200
    )
    wc.generate(" ".join(seg_list))
    wc.to_file("ciyun.jpg")
    plt.imshow(wc, interpolation="bilinear")

def word_cloud():
    result_word=[]
    stop_word=["\r\n","\n"]
    with open("./stopwords.txt","rb") as file_read:
        line=file_read.readline()
        line=str(line,"utf-8").replace("\r\n","").replace("\n","")
        while line:
            stop_word.append(line)
            line=file_read.readline()
            line=str(line,"utf-8").replace("\r\n","").replace("\n","")
    with open("./info.txt","rb") as file_read:
        line=file_read.readline()
        line=str(line,"utf-8")
        while line:
            for word in jieba.cut(line):
                if word not in stop_word:
                    result_word.append(word)
            line=file_read.readline()
            line=str(line,"utf-8")
    drawWordCloud(result_word)
    
def cluster_report():
    dicts=cluster()
    words=word_frequency().most_common(50)
    nums={}
    for key,value in words:
        nums[key]=value
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.figure(figsize=(10,12)) 
    labels = ["第"+str(key+1)+"类" for key in range(25)]
    sizes = [] 
    for key,value in dicts.items():
        pty=0
        for word in value:
            pty=pty+nums[word]
        sizes.append(pty)
    a = np.random.rand(1,26)
    color_vals = list(a[0])
    my_norm = mpl.colors.Normalize(-1, 1) # 将颜色数据的范围设置为 [0, 1]
    my_cmap = mpl.cm.get_cmap('rainbow', len(color_vals)) # 可选择合适的colormap，如：'rainbow'
    patches,text1,text2 = plt.pie(sizes,
                      labels=labels,
                      colors=my_cmap(my_norm(color_vals)),
                      labeldistance = 1.2,
                      autopct = '%3.2f%%', 
                      shadow = False, 
                      startangle =90, 
                      pctdistance = 0.6) 
    plt.axis('off')
    plt.legend(patches, labels, loc='center left')
    plt.tight_layout()
    plt.axis('equal')
    plt.legend()
    plt.savefig('./2.png') 
    plt.show()