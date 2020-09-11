'''
计算词向量集合，根据用户搜索的词语返回相似的关键词
'''
#!/usr/bin/env Python3
# coding=utf-8
from bs4 import BeautifulSoup
import jieba
import pyodbc
from gensim.models import word2vec
from gensim import models
import logging
import json
import os
import re
import threading
from make_invert_index import make_stop_list


stop_list1 = make_stop_list('./词典/停用词1.txt')
stop_list2 = make_stop_list('./词典/停用词2.txt')
stop_list = stop_list1 + stop_list2
stop_list.append('\n')
stop_list.append('')

mutex = threading.Lock()
database = 'dbo.file_table'
conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-RQTO7L9;DATABASE=lcd_test;UID=sa;PWD=Soda.123')
rsor = conn.cursor()


def get_all_files(dir):
    files_ = []
    list = os.listdir(dir)
    for i in range(0, len(list)):
        path = os.path.join(dir, list[i])
        if os.path.isdir(path):
            files_.extend(get_all_files(path))
        if os.path.isfile(path):
            files_.append(path)
    return files_

def set_words():

    words_list = []
    
    with mutex:
        rsor.execute("select simi_word from file_table order by f_id")
        sentences = rsor.fetchall()
        for sentence in sentences:
            # print(type(sentence[0]),sentence[0])
            sent = json.loads(sentence[0])
            aa = []
            for i in sent:
                if len(i) <= 21:
                    i = i.upper()
                    if i not in stop_list:
                        aa.append(i)
            words_list.append(aa)


    with open('./词典/语料库.txt', 'w', encoding = 'utf-8') as f:
        for wl in words_list:
            for ii in wl:
                f.write(ii + ' ')
            f.write('\n')

def train():

    logging.basicConfig(format = '%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)
    #训练word2vec模型
    sentences = word2vec.Text8Corpus(r"词典\语料库.txt") #加载语料库
    model = word2vec.Word2Vec(sentences, size = 400, window = 10, min_count = 1)  #训练skip-gram模型，默认window=5
    print (model)

    #保存模型
    model.save("words_model/model_word.model")
    # 对应的加载方式
    # model_2 = word2vec.Word2Vec.load("text8.model")

    # 以一种 C语言可以解析的形式存储词向量  
    model.wv.save_word2vec_format("words_model/model_word.bin", binary = True)
    # 对应的加载方式
    # model_3 = word2vec.Word2Vec.load_word2vec_format("text8.model.bin", binary=True)

def go(word):
    similiar_dict = dict()
    model = word2vec.Word2Vec.load("words_model/model_word.model")
    word = word.upper()
    try:
        res = model.most_similar(word, topn = 5)
        for item in res:
            similiar_dict[item[0]] = item[1]
        # print('{}的相似词有{}\n'.format(word,similiar_dict))
        return similiar_dict
    except Exception as e:
        print('{}'.format(e))
        return None


if __name__ == "__main__":
    # pass
    set_words()
    train()
    model = word2vec.Word2Vec.load("words_model/model_word.model")
    while True:
        word = input('输入一个词语：').upper()
        if word == 0:
            break
        else:
            res = model.most_similar(word, topn = 10)
            for item in res:
                print(item[0] + "," + str(item[1]))
    