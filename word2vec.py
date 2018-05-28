# -*- coding: utf-8 -*-
from gensim import models
import os
import logging
import jieba

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

train_dir = "./word2vec"

class Sentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for filename in os.listdir(self.dirname):
            file_path = self.dirname + "/" + filename
            for line in open(file_path,"rb"):
                try:
                    line=str(line,"utf-8")
                except:
                    pass
                words = jieba.cut(line)
                result_word = []
                for word in words:
                    if word not in["、","，","\n","访客"]:
                        result_word.append(word)
                yield result_word

sentences = Sentences(train_dir)
model = models.Word2Vec(sentences, workers=20, min_count=50, size=300)

model.save("./word2vec/word2vec_model")