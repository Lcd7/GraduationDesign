#! -*- coding:utf-8 -*-
import json
from bs4 import BeautifulSoup
import copy

# lll = dict()
# lll['几秒手工'] = 6
# lcd = json.dumps(lll,ensure_ascii=False)
# print(lll)
# print(type(lcd))
# print(lcd)

# with open ('django.json', 'r') as f:
#     js = json.load(f)
#     print(type(js))
#     print(js)


# path = r'C:\Users\lcd\Desktop\基于自然语言处理的索引型知识库\html文件\ASP教程\AJAX简介.html'
# #打开文件
# htmlfile = open(path, 'r', encoding = 'utf-8')
# #读取html句柄
# htmlhandle = htmlfile.read()
# #解析html
# soup = BeautifulSoup(htmlhandle, 'lxml')
# h1 = ''
# for _h1 in soup.find_all('html'):
#     h1 += _h1.get_text()
# h1 = h1.replace('\n','').replace('\t','')
# print(h1)

# import os
# def find_trouble_file(file_dir):
#     for root, dirs, files in os.walk(file_dir):
#         # print('root_dir:', root)  # 当前目录路径
#         # print('sub_dirs:', dirs)  # 当前路径下所有子目录
#         # print('files:', files[:5])  # 当前路径下所有非目录子文件
#         # print('\n')
#         if files:
#             main_file = []
#             for _file in files:
#                 if 'a' not in _file and '源文件' in root:
#                     main_file.append(_file)

#             if len(main_file) > 1:
#                 print(root)
#                 with open('同一文号含有两个主件的文件.txt', 'a' , encoding = 'utf-8') as f:
#                     for i in main_file:
#                         f.writelines('{}\n'.format(i))

# find_trouble_file(r'C:\Users\lcd\Desktop\111')


def Merge(dict1, dict2): 
    res = {**dict1, **dict2} 
    return res 
      
# 两个字典
dict1 = {'a': 10, 'b': 8, 'd': 4} 
dict2 = {'d': 6, 'c': 4} 
dict3 = Merge(dict1, dict2) 
print(dict3)