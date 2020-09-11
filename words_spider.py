'''
爬取 汉辞网 在线词典
'''
from selenium import webdriver
import time
import re
alphalist = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t','w','x','y','z']
def find_source(dr):
    source = dr.find_element_by_xpath('//*[@id="table1"]/tbody')
    strs = source.get_attribute('innerHTML')
    strs = strs.replace('</strong>','</p>')
    strs = strs.replace('</a>','</p>')
    strs = strs.replace('</div>','</p>')
    strs = strs.replace('</br>','</p>')
    strs = strs.replace('<br>','</p>')
    strs = strs.replace('</span>','</p>')
    strs = strs.replace('</font>','</p>')
    strs = strs.replace('<td>','')
    strs = strs.replace('</td>','')
    strs = strs.replace('<tr>','')
    strs = strs.replace('</tr>','')
    strs = re.sub(r'<img\b[^<>]*>','',strs)
    strs = re.sub(r'</img\b[^<>]*>','',strs)
    strs = re.sub(r'<font\b[^<>]*>','',strs)
    strs = re.sub(r'<span\b[^<>]*>','',strs)
    strs = re.sub(r'<p\b[^<>]*>','',strs)
    strs = re.sub(r'<a\b[^<>]*>','',strs)
    strs = re.sub(r'<div\b[^<>]*>','',strs)
    strs = re.sub(r'<brstyle\b[^<>]*>','',strs)
    strs = strs.replace(" ",'')
    strs = strs.replace("\n",'')
    strs = strs.replace(u"&ensp;",'')
    strs = strs.replace(u"&nbsp;",'')
    strs = strs.replace(u"\u2002",'')
    strs = strs.replace(u"\u3000",'')
    
    return strs

for alpha in alphalist:
    dr = webdriver.Chrome()
    dr.maximize_window()
    dr.get('http://www.hydcd.com/cidian/index_{}.htm'.format(alpha))
    dr.implicitly_wait(10)
    wordlist = []
    wordstr = find_source(dr)
    strlist = wordstr.split('</p>')
    for nu in strlist:
        if nu == ''\
            or nu == ' ':
            strlist.remove(nu)
    for nu in strlist:
        if nu == ''\
            or nu == ' ':
            strlist.remove(nu)
    for word in strlist:
        wordlist.append(word)
    with open ('./词典/汉辞网词典.txt', 'a', encoding = 'utf-8') as f:
        for wd in wordlist:
            f.writelines(wd + '\n')
    wordlist.clear()
    dr.quit()