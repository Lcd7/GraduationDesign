
'''
把词库里的词分成词长度分别为2到8的七个子词典（列表）
再存入数据库
'''
def dictionaries():
    dict_list = []
    with open('./词典/ch_dict.txt', 'r', encoding = 'utf-8') as f:
        _list = f.readlines()
    for word in _list:
        new_word = word.replace('\n','')
        dict_list.append(new_word)
    dict_list2, dict_list3, dict_list4, dict_list5, dict_list6, dict_list7, dict_list8 = [],[],[],[],[],[],[]
    for item in dict_list:
        if len(item) == 2:
            dict_list2.append(item)
        if len(item) == 3:
            dict_list3.append(item)
        if len(item) == 4:
            dict_list4.append(item)
        if len(item) == 5:
            dict_list5.append(item)
        if len(item) == 6:
            dict_list6.append(item)
        if len(item) == 7:
            dict_list7.append(item)
        if len(item) == 8:
            dict_list8.append(item)
    return dict_list2, dict_list3, dict_list4, dict_list5, dict_list6, dict_list7, dict_list8
            
