'''
把本地html文件存入数据库。
'''
import pyodbc
from bs4 import BeautifulSoup
import os
import threading
import jieba
import json
import re

def remove_null(_list):
    for _ in range(5):
        for i in _list:
            if i == '':
                _list.remove(i)
    return _list

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


mutex = threading.Lock()
database = 'dbo.file_table'
conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-RQTO7L9;DATABASE=lcd_test;UID=sa;PWD=Soda.123')
rsor = conn.cursor()


creat_table = """create table file_table
(
   id                   int not null auto_increment,
   name                 varchar(255),
   file_text            varchar(MAX),
   primary key (id)
)"""
# with mutex:
#     rsor.execute("create table file_table (id int identity(1,1) not null, file_name varchar(255), file_path varchar(255) not null, file_words varchar(MAX) not null)")
# rsor.execute("insert into file_table(file_name,file_text) values({},{})".format())
# conn.commit()
path = r'D:\Code\Code\Code\基于自然语言处理的索引型知识库\html文件'
files_list = get_all_files(path)

for ff in files_list:
    _, fname = os.path.split(ff)
    fname = fname.replace(r'.html','')
    #打开文件
    htmlfile = open(ff, 'r', encoding = 'utf-8')
    #读取html句柄
    htmlhandle = htmlfile.read()
    #解析html
    soup = BeautifulSoup(htmlhandle, 'lxml')
    text = ''
    for _html in soup.find_all('p'):
        text += _html.get_text()
    text = text.replace('\n','').replace('\t','').replace("\'", '')
    text = re.sub(r'<[^>]*>', '', text)
    # reg1 = "[^0-9A-Za-z\u4e00-\u9fa5]"  #去符号
    # text = re.sub(reg1, '', text)

    #对文本切词存入数据库
    # seg_list = jieba.cut(text, cut_all = True)
    # word_list = []
    # for i in seg_list:
    #     word_list.append(i)
    # word_list = remove_null(word_list)
    # words_str = json.dumps(word_list, ensure_ascii = False)
    # with mutex:
    #     rsor.execute("insert into file_table(file_name, file_path, file_words) values(?,?,?)",(fname, ff, words_str))
    #     conn.commit()

    #对文本切词存入数据库(用于计算词语相似度)
    seg_list = jieba.cut(text, cut_all = False)
    word_list = []
    for i in seg_list:
        if i != ' ':
            word_list.append(i)
    word_list = remove_null(word_list)
    words_str = json.dumps(word_list, ensure_ascii = False)
    with mutex:
        sql = "update file_table set simi_word = '{}' where file_name = '{}'".format(words_str, fname)
        rsor.execute(sql)
        conn.commit()

    # 将正文P标签内容存入数据库
    with mutex:
        sql = "update file_table set content = '{}' where file_name = '{}'".format(text, fname)
        rsor.execute(sql)
        conn.commit()
