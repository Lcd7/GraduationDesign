#! -*- coding:utf-8 -*-
'''
构建倒排索引
'''
import jieba
import os
import json
import pyodbc
import threading
import make_dictionary
import copy


mutex = threading.Lock()
database = 'dbo.file_table'
conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-RQTO7L9;DATABASE=lcd_test;UID=sa;PWD=Soda.123')
rsor = conn.cursor()


def make_stop_list(dir):
    _list = []
    new_list = []
    with open(dir, 'r', encoding = 'utf-8') as f:
        _list = f.readlines()
    for word in _list:
        new_word = word.replace('\n','')
        new_list.append(new_word)
    return new_list
    
def removeNousefulWords(_set):
    _set2 = copy.deepcopy(_set)
    global stop_list
    for _ in range(3):
        for i in _set:
            if i[0] == '#' or len(i) == 1:
                try:
                    _set2.remove(i)
                except:
                    pass
                # except KeyError as err:
                #     print(err)

    _set2 = _set2.difference(set(stop_list))
    return _set2
    
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

def upper_index():
    new_index = dict()
    with open(r'./index/text_invert_index.json', 'r', encoding = 'utf-8') as f:
        title_index = json.load(f)
        for key, values in title_index.items():
            key = key.upper()
            if key not in new_index:
                new_index[key] = values
            else:
                for vk, vvs in values.items():
                    if vk not in new_index[key]:
                        new_index[key][vk] = vvs
                    else:
                        new_index[key][vk] = new_index[key][vk] + vvs

    json_new_index_str = json.dumps(new_index, ensure_ascii = False)
    with open(r'./index/111text_invert_index.json', 'w', encoding = 'utf-8') as f:
        f.write(json_new_index_str)
# upper_index()

if __name__ == "__main__":
    pass
    #所有可能得分词
    # seg_list = jieba.cut("我来到北京清华大学", cut_all = True)
    # for i in seg_list:
    #     print(i)
    #只分一次的分词
    # seg_list = jieba.cut("我来到北京清华大学")
    # print(seg_list)


    #建立停用词
    stop_list1 = make_stop_list('./词典/停用词1.txt')
    stop_list2 = make_stop_list('./词典/停用词2.txt')
    stop_list = stop_list1 + stop_list2
    stop_list.append('\n')
    stop_list.append('')

    all_words = []
    all_title = []

    #读取文件  提取词向量
    with mutex:
        rsor.execute("select * from file_table order by f_id")
        text = rsor.fetchall()

    for sentence in text:
        # 正文词向量集合
        # stce = sentence[3]
        # for i in jieba.cut(stce, cut_all = True):
        #     if i not in stop_list:
        #         all_words.append(i)
        #标题词向量集合
        tit = sentence[1]
        for i in jieba.cut(tit, cut_all = True):
            all_title.append(i.upper())

    # #去掉停用词
    set_all_title = set(all_title)
    # set_all_words = set(all_words)
    # set_all_words = removeNousefulWords(set_all_words)


    # 构建倒排索引
    title_index = dict()
    for wd in set_all_title:
        ch_dict = dict()
        for tl in text:
            num_wd = 0
            title = tl[1]
            for i in jieba.cut(title, cut_all = True):
                i = i.upper()
                if wd == i:
                    num_wd += 1
            if num_wd != 0:
                ch_dict[tl[0]] = num_wd
        if ch_dict:
            title_index[wd] = ch_dict
        del ch_dict
    json_title_index_str = json.dumps(title_index, ensure_ascii = False)
    with open ('./index/text_title_index11111111111.json', 'w', encoding = 'utf-8') as f:
        f.write(json_title_index_str)  

    # invert_index = dict()
    # num_word = 1
    # for wd in set_all_words:
    #     if num_word % 100 == 0:
    #         print(str(num_word/len(set_all_words)*100)[:6] + '%')
    #     # temp = []
    #     ch_dict = dict()
    #     for fl in text:
    #         num_wd = 0
            
    #         for i in json.loads(fl[3]):
    #             # i = i.upper()
    #             if wd == i:
    #                 num_wd += 1
    #         if num_wd != 0:
    #             ch_dict[fl[0]] = num_wd
    #     if ch_dict:
    #         invert_index[wd] = ch_dict
    #     del ch_dict  
    #     num_word += 1 
    # json_invert_index_str = json.dumps(invert_index, ensure_ascii = False)
    # with open ('./index/text_invert_index1111111111111.json', 'w', encoding = 'utf-8') as f:
    #     f.write(json_invert_index_str)  

