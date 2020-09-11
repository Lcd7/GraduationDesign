import make_dictionary
import re

dict_list2, dict_list3, dict_list4, dict_list5, dict_list6, dict_list7, dict_list8 = \
    make_dictionary.dictionaries()

dict_list = ['', '', dict_list2, dict_list3, dict_list4, dict_list5, dict_list6, dict_list7, dict_list8]

def MMcompared(substr):
    l = len(substr)
    while l > 1:
        for i in range(l, 1,-1):
            if l == int('{}'.format(i)):
                if substr in dict_list[i]:
                    return substr, l
                else:
                    l -= 1
                    substr = substr[:-1]
    else:
        return substr, l

def MM(test):
    reg1 = "[^0-9A-Za-z\u4e00-\u9fa5]"  #去符号
    # reg2 = "[^A-Za-z0-9\!\%\[\]\,\。]"  #去英文字符
    test = re.sub(reg1, '', test)
    # print(test)
    # test = re.sub(reg2, '', test)
    # print(test)
    maxlength, index = 8, 8
    wordlist = []
    while test:
        if len(test) >= maxlength:
            index = 8
        else:
            index = len(test)
        substr = test[0:index]
        word, num = MMcompared(substr)
        wordlist.append(word)
        test = test[num:]
    # print(wordlist)
    return wordlist

def FMMcompared(substr):
    l = len(substr)
    while l > 1:
        for i in range(l, 1,-1):
            if l == int('{}'.format(i)):
                if substr in dict_list[i]:
                    return substr, l
                else:
                    l -= 1
                    substr = substr[1:]
    else:
        return substr, l

def FMM(test):
    reg1 = "[^0-9A-Za-z\u4e00-\u9fa5]"  #去符号
    # reg2 = "[^A-Za-z0-9\!\%\[\]\,\。]"  #去英文字符
    test = re.sub(reg1, '', test)
    # test = re.sub(reg2, '', test)
    maxlength, index = 8, 8
    wordlist = []
    while test:
        if len(test) >= maxlength:
            index = 8
        else:
            index = len(test)
        substr = test[-index:]
        word, num = FMMcompared(substr)
        wordlist.append(word)
        test = test[:-num]
    resultlist = wordlist[::-1]
    # print(resultlist)
    return resultlist

def better(result1, result2):
    result = []
    if result1 == result2:
        return result1
    else:
        len1 = len(result1)
        len2 = len(result2)
        ambiguity = ''
        if len1 == len2:
            for i in range(len1):
                if result1[i] == result2[i]:
                    if ambiguity:
                        result.append(ambiguity)
                        result.append(result1[i])
                    else:
                        result.append(result1[i])
                    ambiguity = ''
                else:
                    ambiguity += result1[i]
            return result
        else:
            return result2

# print(MM('中华人民共和国资源税法'))