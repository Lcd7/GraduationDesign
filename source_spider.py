'''
爬虫爬取网络文章资源
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from lxml import etree
import requests
import re
import os

def remove_str(strs):
    strs = strs.replace('<','[')
    strs = strs.replace('>',']')
    strs = strs.replace('\t','')
    strs = strs.replace('\n','')
    strs = strs.replace('\r','')
    strs = strs.replace(' ','')
    return strs

def make_dir(path):
    #创建文件夹
    path = path.strip()
    path = path.rstrip("\\")

    folder = os.path.exists(path)
    #判断结果
    if not folder:
        #如果不存在，则创建新目录
        os.makedirs(path)
    else:
        pass

def get_source(dr, url):
    dr.get(url)
    dr.implicitly_wait(10)
    directory = dr.find_element_by_xpath('//div[@class = "tab"]').text
    directory = remove_str(directory)
    make_dir('./html文件/' + directory)
    # make_dir('./文本文件/' + directory)
    #courses = dr.find_elements_by_xpath('//div[@id = "leftcolumn"]/a')
    courses = dr.find_elements_by_xpath('//ul[@class = "membership"]//a')
    hrefs = []
    for _link in courses:
        if _link.get_attribute('href')[:4] != 'http':
            _href = _link.get_attribute('href') + 'https://www.runoob.com'
        else:
            _href = _link.get_attribute('href')
        hrefs.append(_href)
    for _link in hrefs:
        try:
            time.sleep(3)
            #请求
            dr.get(_link)
            dr.implicitly_wait(20)
            #标题
            # try:
                # title = dr.find_element_by_xpath('//div[@id = "content"]/h1').text
            title = dr.find_element_by_xpath('//div[@class = "article-heading"]/h2').text
            # except:
            #     title = dr.find_element_by_xpath('//div[@id = "content"]/h2').text
            title = remove_str(title)
            folder = os.path.exists('./html文件/' + directory + '/' + title + '.html')
            if not folder:
                #正文
                # content = dr.find_element_by_id('content').get_attribute('innerHTML')
                content = dr.find_element_by_class_name('article-intro').get_attribute('innerHTML')
                # content_text = dr.find_element_by_id('content').text
                #保存
                with open('./html文件/' + directory + '/' + title + '.html', 'w', encoding = 'utf-8') as f:
                    f.writelines(content)
                    #aaa = directory + '/' + title + '.html'
                    #print('保存文件{}'.format(aaa))
                # with open('./文本文件/' + directory + '/' + title + '.txt', 'w', encoding = 'utf-8') as f:
                #     f.writelines(content_text)
                print(title)
            else:
                print("*")
        except:
            pass


# headers ={
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
#     'Connection':'close'
#     }

dr = webdriver.Chrome()
dr.maximize_window()
dr.get('https://www.runoob.com')
dr.implicitly_wait(10)

# android_list = dr.find_elements_by_xpath('/html/body/div[3]/div[1]/div[3]/div/ul/li/a')

for i in [5]:      #缺5模块
    clicks = dr.find_elements_by_xpath('/html/body/div[4]/div/div[2]/div[{}]/a'.format(i))
    # print(clicks)
    _clicks = []
    for url in clicks:
        if url.get_attribute('href')[:4] != 'http':
            url = 'https://www.runoob.com' + url.get_attribute('href')
        else:
            url = url.get_attribute('href')
        _clicks.append(url)
    for url in _clicks[:1]:         #第几篇课程
        try:
            get_source(dr, url)
        except:
            time.sleep(5)
            dr.refresh()
            get_source(dr,url)
        