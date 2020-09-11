#! -*- coding:utf-8 -*-
'''
数据库的词
网上下载的词典进行汇总存在ch_dict.txt里面
'''
import pyodbc
import threading
import json

list1, list2, list3 = [], [], []

mutex = threading.Lock()
database = 'dbo.file_table'
conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-RQTO7L9;DATABASE=lcd_test;UID=sa;PWD=Soda.123')
rsor = conn.cursor()

with mutex:
    rsor.execute("select * from file_table order by f_id")
    text = rsor.fetchall()

for words in text:
    list3 += json.loads(words[3])


with open('./词典/汉辞网词典.txt', 'r', encoding = 'utf-8') as f:
    _list1 = f.readlines()
    for word in _list1:
        new_word = word.replace('\n','')
        list1.append(new_word)


with open('./词典/下载词典1.txt', 'r', encoding = 'utf-8') as f:
    _list2 = f.readlines()
    for word in _list2:
        new_word = word.replace('\n','')
        list2.append(new_word)

        
sum_list = list(set(list1 + list2 + list3))
with open('./词典/ch_dict.txt', 'w', encoding = 'utf-8') as f:
    for wd in sum_list:
        wd = wd.upper()
        f.writelines("{}\n".format(wd))