import re
import algorithm
# import view
import search_file
import json
import servers
import os

search = ''

with open ('./index/text_invert_index.json', 'r', encoding = 'utf-8') as f:
    # invert_index = json.loads(f.read())
    invert_index = json.load(f)

with open ('./index/text_title_index.json', 'r', encoding = 'utf-8') as f:
    title_index = json.loads(f.read())

def main(text):
    global invert_index
    global title_index
    global search
    search = text.upper()
    search = search.replace('，','').replace('，','')

    result1 = algorithm.MM(search)
    result2 = algorithm.FMM(search)
    result = algorithm.better(result1, result2)

    # print(result)
    _path = search_file.do_search(result, title_index, invert_index)

    if _path:
        return _path, result
    else:
        return None
    
if __name__ == "__main__":
    main('python')
    # os.system('python servers.py')
    # view.show_it()
    # a = 'pYthon.撒反对'
    # a = a.upper()
    # print(a)