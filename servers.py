from flask import Flask, redirect, url_for, request, render_template
import main
# from main import title_index, invert_index
from flask_restful import Resource,Api
from flask_cors import *
import os
import similarity
import search_file
import algorithm
import json
from urllib import parse

with open ('./index/text_invert_index.json', 'r', encoding = 'utf-8') as f:
    # invert_index = json.loads(f.read())
    invert_index = json.load(f)

with open ('./index/text_title_index.json', 'r', encoding = 'utf-8') as f:
    title_index = json.loads(f.read())

with open('key_words/key_words200119.json', 'r', encoding = 'utf-8') as f:
    key_words = json.loads(f.read())

def get_files_name(file_dir):
    file_list = []
    for _, _, files in os.walk(file_dir):
        for _file in files:
            file_list.append(_file)
    return file_list



app = Flask(__name__)
CORS(app,supports_credentials=True)

api = Api(app)

#用户搜索
class Search(Resource):
    '''
    用户输入搜寻
    '''

    @staticmethod
    def get():
        result = dict()
        result['code'] = 200
        searchkey = request.args.get('searchkey').upper()
        searchkey = parse.unquote(searchkey)
        # page = request.args.get('page')
        # result['page'] = page
        # result['searchkey'] = searchkey

        text = searchkey
        if text:
            text = text.replace(' ','').upper()
            try:
                _path, sentence = main.main(text)     #html文件路径(列表)
                print(sentence)
                result['sentence'] = sentence

                if _path:
                    file_name_list = []
                    # print(_path)
                    for i in _path:
                        
                        file_name = i[0]#.encode('utf-8').decode('unicode_escape')
                        file_content = str(i[1])
                        file_name_list.append([file_name, file_name.split('\\')[-1].split('.')[0], file_content])

                    result['file_name_list'] = file_name_list
                    # result['file_len'] = len(file_name_list)
                    # result['flag'] = 1
                else:
                    result['file_name_list'] = None
            except:
                result['file_name_list'] = None
                result['sentence'] = ''


        #计算相似词
        global title_index, invert_index
        _path1 = []
        simi_dict = dict()

        # searchkey = request.args.get('searchkey').upper()   #可能是一句话
        
        result1 = algorithm.MM(searchkey)
        result2 = algorithm.FMM(searchkey)
        result_words = algorithm.better(result1, result2)

        # print('切词结果：{}\n'.format(result_words))

        for rw in result_words:
            flag = similarity.go(rw)
            if flag is not None:
                simi_dict.update(flag)    #每个词语反5个相似词   dict
            else:
                pass

        sort_simi = sorted(simi_dict.items(), key = lambda x:x[1], reverse = True)
        simi_words = []
        for i in range(5):
            simi_words.append(sort_simi[i][0])
        result['simi_words'] = simi_words

        print('关键词排序：{}\n'.format(sort_simi))

        for key, _ in sort_simi:
            simi_list = []
            simi_list = search_file.search_similiar(key, title_index, invert_index)  #每个相似词返回两个文章
            if type(simi_list) == list:
                _path1 += simi_list
        # print('相似文件：{}\n'.format(_path1))
        if _path1:
            result['similiar_word_path'] = _path1
        else:
            result['similiar_word_path'] = None


        #关键词
        if result['sentence']:
            global key_words
            key_word_file_list = []
            for term in result['sentence']:
                if term.upper() in key_words:
                    key_word_file_list_num = 0
                    for key_word_file_path in key_words[term.upper()]:
                        key_file_name = key_word_file_path.split('\\')[-1][:-5]
                        key_word_file_list.append([key_file_name, key_word_file_path])
                        key_word_file_list_num += 1
                        if key_word_file_list_num == 2:
                            break
            result['key_word_files'] = key_word_file_list
        else:
            result['key_word_files'] = None
        return result

#用户选择语言
class switchLanguage(Resource):
    '''
    用户点击选择需要查看的语言教程
    '''
    @staticmethod
    def get():
        result = dict()
        result['code'] = 200
        _path = []
        chooseLanguage = request.args.get('language').upper()
        chooseLanguage = parse.unquote(chooseLanguage)
        # print(chooseLanguage,len(chooseLanguage))
        if chooseLanguage == 'PYTHON3':
            py_list = []
            py_list = get_files_name(r'D:\Code\基于自然语言处理的索引型知识库\html文件Python3教程')
            _path = search_file.choose_search(py_list,)
            

        elif chooseLanguage == 'JAVA':
            ja_list = []
            ja_list = get_files_name(r'D:\Code\基于自然语言处理的索引型知识库\html文件Java教程')
            _path = search_file.choose_search(ja_list)
            

        elif chooseLanguage == 'HTML':
            ht_list = []
            ht_list = get_files_name(r'D:\Code\基于自然语言处理的索引型知识库\html文件HTML教程')
            _path = search_file.choose_search(ht_list)
            

        elif chooseLanguage == 'DOCKER':
            vb_list = []
            vb_list = get_files_name(r'D:\Code\基于自然语言处理的索引型知识库\html文件Docker教程')
            _path = search_file.choose_search(vb_list)
            

        elif chooseLanguage == 'GO':
            go_list = []
            go_list = get_files_name(r'D:\Code\基于自然语言处理的索引型知识库\html文件Go语言教程')
            _path = search_file.choose_search(go_list)
            

        elif chooseLanguage == 'PHP':
            php_list = []
            php_list = get_files_name(r'D:\Code\基于自然语言处理的索引型知识库\html文件PHP教程')
            _path = search_file.choose_search(php_list)
            

        elif chooseLanguage == 'RUBY':
            ruby_list = []
            ruby_list = get_files_name(r'D:\Code\基于自然语言处理的索引型知识库\html文件Ruby教程')
            _path = search_file.choose_search(ruby_list)
            

        elif chooseLanguage == 'JSP':
            jsp_list = []
            jsp_list = get_files_name(r'D:\Code\基于自然语言处理的索引型知识库\html文件JSP教程')
            _path = search_file.choose_search(jsp_list)
            

        elif chooseLanguage == 'DJANGO':
            dj_list = []
            dj_list = get_files_name(r'D:\Code\基于自然语言处理的索引型知识库\html文件Django教程')
            _path = search_file.choose_search(dj_list)
            
        # print(_path)
        file_name_list = []
        if _path:
            for i in _path:
                if i[1]:
                    file_name_list.append([i[0], i[0].split('\\')[-1][:-5], i[1]])
        result['file_name_list'] = file_name_list

        return result

#相似度
class similiarWord(Resource):
    @staticmethod
    def get():
        global title_index, invert_index
        _path = []
        simi_dict, result = dict(), dict()
        result['code'] = 200
        searchkey = request.args.get('searchkey').upper()   #可能是一句话
        
        result1 = algorithm.MM(searchkey)
        result2 = algorithm.FMM(searchkey)
        result_words = algorithm.better(result1, result2)

        print('切词结果：{}\n'.format(result_words))

        for rw in result_words:
            flag = similarity.go(rw)
            if flag is not None:

                simi_dict.update(flag)    #每个词语反5个关键词   dict
            else:
                pass

        sort_simi = sorted(simi_dict.items(), key = lambda x:x[1], reverse = True)
        simi_words = []
        for i in range(5):
            simi_words.append(sort_simi[i][0])
        result['simi_words'] = simi_words

        print('关键词排序：{}\n'.format(sort_simi))

        for key, _ in sort_simi:
            simi_list = []
            simi_list = search_file.search_similiar(key, title_index, invert_index)  #每个关键词返回两个文章
            if type(simi_list) == list:
                _path += simi_list
        print('相似文件：{}\n'.format(_path))
        if _path:
            result['similiar_word_path'] = _path
        else:
            result['similiar_word_path'] = None

        return result

#用户选择分类
class findFilesPart(Resource):
    '''
    点击查找课程分类
    '''
    @staticmethod
    def get():
        result = dict()
        result['code'] = 200
        _path = []
        choosepart = request.args.get('choosepart')
        choosepart = parse.unquote(choosepart)
        print(choosepart)
        _path = search_file.choosepartfile(choosepart)
        file_class = set()
        if _path:
            for clas in _path:
                file_class.add(clas[0])
        result['file_class'] = list(file_class)
        # if _path:
        #     part_files = []
        #     for f_p in _path:
        #         f_name = str(f_p[0].split('//')[-1][:-5])
        #         part_files.append([f_p, f_name])
        # result['part_files'] = part_files

        return result


class findFilesClass(Resource):
    '''
    根据点击的文章分类返回文章
    '''
    @staticmethod
    def get():
        result = dict()
        result['code'] = 200
        _path, f_list = [], []

        chooseclass = request.args.get('class_title')
        chooseclass = parse.unquote(chooseclass)
        # print(chooseclass)
        f_dir = r'D:\\Code\\基于自然语言处理的索引型知识库\\html文件\\' + chooseclass
        # print(f_dir)
        f_list = get_files_name(f_dir)
        # print("f_list:{}".format(f_list))
        _path = search_file.choose_search(f_list)
        # print("_path:{}".format(_path))
        file_name_list = []
        if _path:
            for i in _path:
                if i[1]:
                    file_name_list.append([i[0], i[0].split('\\')[-1][:-5], i[1]])
        result['file_name_list'] = file_name_list
        return result
        

api.add_resource(Search, '/search/')
api.add_resource(switchLanguage, '/switch/')
api.add_resource(similiarWord, '/similiar/')
api.add_resource(findFilesPart, '/part/')
api.add_resource(findFilesClass, '/choose/')


if __name__ == "__main__":
    app.run(debug = True)

    
    #手动设置绑定IP、端口。 
    # app.run(host='0.0.0.0', debug=True)

    