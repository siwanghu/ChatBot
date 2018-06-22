# -*- coding: utf-8 -*-
import jieba
from jieba import analyse
from jieba import posseg

def __cut_word(input_str):
    words=[]
    for word in jieba.cut(input_str):
        words.append(word)
    return words

def __extract_keyword_TFidf(input_str):
    keyword=[]
    for key,weight in analyse.extract_tags(input_str,withWeight=True,topK=5):
        if len(key)<=4:
            keyword.append(key)
    return keyword

def __extract_keyword_TextRank(input_str):
    keyword=[]
    for key,weight in analyse.textrank(input_str,withWeight=True,topK=5):
        if len(key)<=4:
            keyword.append(key)
    return keyword

def __word_posseg(input_str):
    wordposseg=[]
    for word,possegs in posseg.cut(input_str):
        if "v" in possegs or "n" in possegs or "a" in possegs:
            wordposseg.append(word)
    return wordposseg

def extract_keyword(input_str):
    keyword=set(__extract_keyword_TFidf(input_str))
    wordposseg=set(__word_posseg(input_str))
    return list(keyword & wordposseg)
print(__cut_word("产品大概多少钱啊"))
print(extract_keyword("产品大概多少钱啊"))
print(__extract_keyword_TFidf("产品大概多少钱啊"))