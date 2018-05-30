# -*- coding: utf-8 -*-
from gensim import models
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = models.Word2Vec.load("./word2vec/word2vec_model")

print(model["会议"])
result = model.most_similar(["会议"])
for value in result:
    print(value[0], value[1])