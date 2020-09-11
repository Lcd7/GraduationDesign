'''
词频TF = 某个词再文章出现的次数/文章的总词数
逆文档频率IDF = log（语料库的文档总数/包含该词的文档数 + 1）
TF-IDF = 词频(TF) * 逆文档频率(IDF)

计算每一篇文章词语的TF-IDF
每篇文章取十个关键词组成关键词集合
用关键词来为用户推荐相关文章
'''


import pyodbc
import threading
import json
import math
import jieba.analyse
from urllib import parse

def make_stop_list(dir):
    _list = []
    new_list = []
    with open(dir, 'r', encoding = 'utf-8') as f:
        _list = f.readlines()
    for word in _list:
        new_word = word.replace('\n','')
        new_list.append(new_word)
    return new_list

def get_key_words1(res, stop_list):
    num_files = len(res)                                        #语料库文档总数
    all_words = []
    TF_IDF_set = set()

    for i in res:                                           #长度大于21的单词不要
        text_words = []
        text_words.append(i[0])
        for text in json.loads(i[1]):
            if len(text) < 21 and text not in stop_list:
                text_words.append(text)                     #去停用词
        all_words.append(text_words)

    for terms in all_words[:5]:
        sort_file_TF_IDF_dict = []
        file_TF_IDF_dict = {}

        for term in terms[1:]:
            include_word_nums = 0
            including_word_in_file_num = terms.count(term)       #单词在文章中的出现次数

            words_tf = including_word_in_file_num / len(terms)

            for file in all_words:                              #计算包含该词的文档数
                if term in file:
                    include_word_nums += 1

            words_idf = math.log(num_files / (include_word_nums + 1))

            TF_IDF = words_tf * words_idf
            file_TF_IDF_dict[term] = [TF_IDF, terms[0]]

        sort_file_TF_IDF_dict = sorted(file_TF_IDF_dict.items(), key = lambda x:x[1][0], reverse = True)
        print(sort_file_TF_IDF_dict[:10])
        for key_word in sort_file_TF_IDF_dict[:10]:
            TF_IDF_set.add(key_word[0])

    with open('key_words/key_words.txt', 'w', encoding = 'utf-8') as f:
        for key_word in TF_IDF_set:
            f.write('{}\n'.format(key_word.upper()))

def get_key_words2(res, stop_list, mutex, rsor):
    
    for i in res:
        l1 = []
        keywords_tfidf = jieba.analyse.extract_tags(i[2], topK = 30)
        num = 0
        for key_word in keywords_tfidf:
            if key_word not in stop_list and key_word not in l1:
                l1.append(key_word)
                num += 1
                if num == 10:
                    break
        sentence = ''
        for term in l1:
            sentence += term.upper() + ','
        sql = "update file_table set key_words = '{}' where f_id = {}".format(sentence, i[0])
        with mutex:
            rsor.execute(sql)
            rsor.commit()
        # print(sql)
        # print(l1)
    # with open('key_words/key_words1.txt', 'w', encoding = 'utf-8')as f:
    #     for i in l1:
    #         f.write('{}\n'.format(i))

def addition():
    with open('key_words/key_words.txt', 'r', encoding = 'utf-8') as f:
        terms1 = f.readlines()
    with open('key_words/key_words1.txt', 'r', encoding = 'utf-8') as f:
        terms2 = f.readlines()
    terms = set(terms1 + terms2)
    with open('key_words/key_words3.txt', 'w', encoding = 'utf-8') as f:
        for i in terms:
            f.writelines('{}'.format(i))



if __name__ == "__main__":
    mutex = threading.Lock()
    database = 'dbo.file_table'
    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-RQTO7L9;DATABASE=lcd_test;UID=sa;PWD=Soda.123')
    rsor = conn.cursor()

    with mutex:
        # sql = "select f_id, simi_word, content from file_table"
        sql = "select file_path, key_words from file_table"
        rsor.execute(sql)
        res = rsor.fetchall()

    stop_list1 = make_stop_list('./词典/停用词1.txt')
    stop_list2 = make_stop_list('./词典/停用词2.txt')
    stop_list = stop_list1 + stop_list2
    stop_list.append('\n')
    stop_list.append('')

    # get_key_words1(res, stop_list)
    # get_key_words2(res, stop_list, mutex, rsor)
    # addition()

    # with open('key_words/key_words3.txt', 'r', encoding = 'utf-8') as f:
    #     low = f.readlines()
    # with open('key_words/key_words3.txt', 'w', encoding = 'utf-8') as f:
    #     for i in low:
    #         i = i.upper()
    #         f.writelines(i)

    #把关键词存到本地json
    # print(res[:5])
    # key_words_dict = {}
    # for item in res:
    #     key_words_list = item[1][:-1].split(',')
    #     for key_word in key_words_list:
    #         key_word = parse.unquote(key_word)      #转成中文字符
    #         if key_word not in key_words_dict:
    #             key_words_dict[key_word] = []
    #         key_words_dict[key_word].append(parse.unquote(item[0]))
    
    # with open('key_words/key_words200119.json', 'a', encoding = 'utf-8')as f:
    #     f.write(json.dumps(key_words_dict))